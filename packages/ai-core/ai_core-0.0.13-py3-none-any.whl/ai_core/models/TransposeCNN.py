import torch
from VerboseLayer import VerboseLayer

class Unflatten(torch.nn.Module):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def forward(self, x):
        return x.view(x.shape[0], *self.size)

class TransposeCNN(torch.nn.Module):
    def __init__(self, 
            channels, 
            linear_layers, 
            kernel_size=3, 
            stride=1, 
            dropout=0.5, 
            output_padding=None,
            unflattened_size=None, # required to unflatten to a correct size
            verbose=False
        ):
        super().__init__()
        l = []

        for idx in range(len(linear_layers) - 1):
            l.extend([
                torch.nn.Linear(linear_layers[idx], linear_layers[idx + 1])
            ])
            l.append(torch.nn.ReLU())   # activate
            # print(idx, len(linear_layers) - 1)
            if idx + 1 == len(linear_layers) - 1: # at the end of the linear layers
                print(unflattened_size)
                l.append(Unflatten(unflattened_size))# unflatten the example

        for idx in range(len(channels) - 1):
            l.append(
                torch.nn.Dropout(dropout)
            )
            if output_padding:
                out_pad = output_padding[idx] # the plus one is to offset the padding. padding remainders are generated from the input layers of the conv, but need to be applied to the output of the transpose conv
            else:
                out_pad = 0
            l.append(
                torch.nn.ConvTranspose2d(channels[idx], channels[idx + 1], kernel_size, stride, output_padding=out_pad)
            )
            if verbose:
                l.append(VerboseLayer(idx))
            l.append(
                torch.nn.BatchNorm2d(channels[idx + 1])
            )
            if idx + 1 != len(channels): # if this is not the last layer ( +1 = zero indexed) (-1 = layer b4 last)
                l.append(torch.nn.ReLU())   # activate
            else:
                l.append(torch.nn.Sigmoid()) # apply sigmoid to put output pixel intensities in real range
 
        self.layers = torch.nn.Sequential(
            *l
        )

    def forward(self, x):
        x = self.layers(x)
        return x