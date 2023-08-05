#%%
import torch
from torch import nn
import torchvision
import os

batch_size = 32
nc = 3 # Number of channels in the training images. For color images this is 3
nz = 100 # Size of z latent vector (i.e. size of generator input)
ngf = 64 # Size of feature maps in generator
ndf = 64 # Size of feature maps in discriminator
lr = 0.0002 # Learning rate for torch.optimizers
beta1 = 0.5 # Beta1 hyperparam for Adam torch.optimizers
# Number of GPUs available. Use 0 for CPU mode.
ngpu = 8

# Decide which device we want to run on
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)

class Generator(nn.Module):
    def __init__(self, ngpu):
        super(Generator, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d( nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d( ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d( ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d( ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh() # GANHACK #1
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self, ngpu):
        super(Discriminator, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(nc, ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4
            nn.Conv2d(ndf * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input)


class GAN:
    def __init__(self):
        self.G = Generator(ngpu).to(device)
        # Handle multi-gpu if desired
        if (device.type == 'cuda') and (ngpu > 1):
            self.G = nn.DataParallel(self.G, list(range(ngpu)))

        # Apply the weights_init function to randomly initialize all weights
        #  to mean=0, stdev=0.2.
        self.G.apply(weights_init)

        # Print the model
        print(self.G)

        # Create the Discriminator
        self.D = Discriminator(ngpu).to(device)

        # Handle multi-gpu if desired
        if (device.type == 'cuda') and (ngpu > 1):
            self.D = nn.DataParallel(self.D, list(range(ngpu)))

        # Apply the weights_init function to randomly initialize all weights
        #  to mean=0, stdev=0.2.
        self.D.apply(weights_init)

        # Print the model
        print(self.D)


    def sample(self, n_examples=64):
        noise = torch.randn(n_examples, nz, 1, 1, device=device)
        # Generate fake image batch with G
        fake = self.G(noise)
        return fake

    def fit(self, dataloader, epochs=100):
        # Initialize BCELoss function
        criterion = nn.BCELoss()

        # Create batch of latent vectors that we will use to visualize
        #  the progression of the generator
        fixed_noise = torch.randn(64, nz, 1, 1, device=device)

        # Establish convention for real and fake labels during training
        real_label = 1.
        fake_label = 0.
        label_noise = 0.3

        # Setup Adam torch.optimizers for both G and D
        torch.optimizerD = torch.optim.Adam(self.D.parameters(), lr=lr, betas=(beta1, 0.999))
        torch.optimizerG = torch.optim.Adam(self.G.parameters(), lr=lr, betas=(beta1, 0.999))
        
        img_list = []
        G_losses = []
        D_losses = []
        iters = 0

        print("Starting Training Loop...")
        for epoch in range(epochs): # For each epoch
            for i, data in enumerate(dataloader, 0): # For each batch in the dataloader

                ############################
                # (1) Update D network: maximize log(D(x)) + log(1 - D(G(z)))
                ###########################
                ## Train with all-real batch
                self.D.zero_grad()
                real_cpu = data[0].to(device) # Format batch
                b_size = real_cpu.size(0)
                label = torch.full((b_size,), real_label, dtype=torch.float, device=device)
                label += (torch.rand_like(label) * label_noise) - (label_noise / 2) # GANHACK #6 soft & noisy labels
                output = self.D(real_cpu).view(-1) # Forward pass real batch through D # GANHACK #4
                errD_real = criterion(output, label) # Calculate loss on all-real batch
                errD_real.backward() # Calculate gradients for D in backward pass
                D_x = output.mean().item()

                ## Train with all-fake batch
                noise = torch.randn(b_size, nz, 1, 1, device=device) # Generate batch of latent vectors
                fake = self.G(noise) # Generate fake image batch with G
                label.fill_(fake_label)
                label += (torch.rand_like(label) * label_noise) - (label_noise / 2) # GANHACK #6 soft & noisy labels
                
                output = self.D(fake.detach()).view(-1) # Classify all fake batch with D # GANHACK #4 = different discriminator loss
                errD_fake = criterion(output, label) # Calculate D's loss on the all-fake batch # GANHACK #2
                errD_fake.backward() # Calculate the gradients for this batch
                D_G_z1 = output.mean().item()
                
                errD = errD_real + errD_fake # Add the gradients from the all-real and all-fake batches
                torch.optimizerD.step() # Update D

                ############################
                # (2) Update G network: maximize log(D(G(z)))
                ###########################
                self.G.zero_grad()
                label.fill_(real_label)  # fake labels are real for generator cost
                # Since we just updated D, perform another forward pass of all-fake batch through D
                output = self.D(fake).view(-1)
                # Calculate G's loss based on this output
                errG = criterion(output, label)
                # Calculate gradients for G
                errG.backward()
                D_G_z2 = output.mean().item()
                # Update G
                torch.optimizerG.step()

                # Output training stats
                if i % 5 == 0:
                    print('[%d/%d][%d/%d]\tLoss_D: %.4f\tLoss_G: %.4f\tD(x): %.4f\tD(G(z)): %.4f / %.4f'
                        % (epoch, epochs, i, len(dataloader),
                            errD.item(), errG.item(), D_x, D_G_z1, D_G_z2))

                # Save Losses for plotting later
                G_losses.append(errG.item())
                D_losses.append(errD.item())

                # Check how the generator is doing by saving G's output on fixed_noise
                if (iters % 500 == 0) or ((epoch == epochs-1) and (i == len(dataloader)-1)):
                    with torch.no_grad():
                        fake = self.G(fixed_noise).detach().cpu()
                    imgs = torchvision.utils.make_grid(fake, padding=2, normalize=True)
                    img_list.append(imgs)
                    # SAVE IMGS
                    print('saving fake imgs')
                    if not os.path.exists('fake_imgs'):
                        os.mkdir('fake_imgs')
                    imgs = torchvision.transforms.ToPILImage()(imgs)
                    imgs.save(f'fake_imgs/step-{iters}.jpeg', 'JPEG')

                iters += 1

