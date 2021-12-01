import src.datasets.wash_fl as wash_fl
import src.train_util as trn

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader

# adapted from https://github.com/ArpitaDutta/Combi-FL/blob/main/rbfnn.py
# and https://github.com/JeremyLinux/PyTorch-Radial-Basis-Function-Layer/blob/master/Torch%20RBF/torch_rbf.py

class RBF(torch.nn.Module):
    def __init__(self, in_features, out_features, basis_func):
        super(RBF, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.centres = torch.nn.Parameter(torch.Tensor(out_features, in_features))
        self.log_sigmas = torch.nn.Parameter(torch.Tensor(out_features))
        self.basis_func = basis_func
        self.reset_parameters()

    def reset_parameters(self):
        torch.nn.init.normal_(self.centres, 0, .001)
        torch.nn.init.constant_(self.log_sigmas, 0)

    def forward(self, input):
        size = (input.size(0), self.out_features, self.in_features)
        x = input.unsqueeze(1).expand(size)
        c = self.centres.unsqueeze(0).expand(size)
        distances = (x - c).pow(2).sum(-1).pow(0.5) / torch.exp(self.log_sigmas).unsqueeze(0)
        return self.basis_func(distances)


# basis functions:
def linear(alpha):
    phi = alpha
    return phi

def sigmoid(alpha):
    phi = torch.nn.functional.sigmoid(alpha)
    return phi

def shifted_sigmoid(alpha):
    phi = torch.mul(torch.sub(sigmoid(alpha), 0.5), 2)
    return phi

if __name__ == '__main__':
    pid = 'Chart'
    bid = '1'
    X, Y, n_lab, d_lab = wash_fl.data_formatted(pid, bid)

    m = RBF(X.shape[1], 1, linear)

    batch_size = 500
    inputs = torch.tensor(X)
    targets = torch.tensor(Y)
    virtual_tests = np.identity(X.shape[1], dtype=np.single)
    dataset = TensorDataset(inputs, targets)
    data_loader = DataLoader(dataset, batch_size, shuffle=True)
    trn.train_fl(m, 1000, data_loader)

    nn_scores = m.forward(torch.tensor(virtual_tests)).detach().numpy().T

