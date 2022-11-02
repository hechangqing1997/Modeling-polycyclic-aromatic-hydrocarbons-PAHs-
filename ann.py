
import torch
import torch.nn as nn
import numpy as np
class ANN(nn.Module):
    def __init__(self, n_feature, n_hidden_layer, n_output):
        super(ANN, self).__init__()
        self.hidden_layer = torch.nn.Linear(n_feature, n_hidden_layer)
        self.output_layer = torch.nn.Linear(n_hidden_layer, n_output)

    def forward(self, x):
        hidden_out = torch.relu(self.hidden_layer(x))
        out = self.output_layer(hidden_out)
        return out

