import torch
from VerboseLayer import VerboseLayer

class CNN(torch.nn.Module):
    def __init__(self, channels, linear_layers, kernel_size=3, stride=1, dropout=0.5, verbose=False, activate_last_linear=False):
        super().__init__()
        l = []

        for idx in range(len(channels) - 1):
            l.append(
                torch.nn.Dropout(dropout)
            )
            l.append(
                torch.nn.Conv2d(channels[idx], channels[idx + 1], kernel_size, stride)                    
            )
            if verbose:
                l.append(VerboseLayer(idx+1))
            l.append(
                torch.nn.BatchNorm2d(channels[idx + 1])
            )
            l.append(torch.nn.ReLU())   # activate
        for idx in range(len(linear_layers) - 1):
            if idx == 0:
                l.append(torch.nn.Flatten())
            l.extend([
                torch.nn.Linear(linear_layers[idx], linear_layers[idx + 1])
            ])
            if activate_last_linear or idx + 1 != len(linear_layers): # if this is not the last layer ( +1 = zero indexed) (-1 = layer b4 last)
                l.append(torch.nn.ReLU())   # activate

        self.layers = torch.nn.Sequential(
            *l
        )

    def forward(self, x):
        x = self.layers(x)
        return x