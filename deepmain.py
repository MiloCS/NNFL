import src.datasets.wash_fl as wash_fl
import src.datasets.fixed as fixed
import os
import numpy as np
from scipy.stats import rankdata
from src.SBFL.sbfl.base import SBFL

import torch
from torch.utils.data import TensorDataset, DataLoader
import src.models as models
import src.train_util as trn

TMP_DIR = 'tmp/'

if __name__=="__main__":
    projects = ['Chart']    #, 'Closure', 'Lang', 'Math', 'Mockito', 'Time'

    for pid in projects:
        project_data_dir = 'data/fault-localization.cs.washington.edu/data/' + pid + '/'
        bug_ids = os.listdir(project_data_dir)
        for bid in bug_ids:
            if int(bid) < 1000:   # if real bug
                print(pid, bid)

                X, Y, n_lab, d_lab = wash_fl.data_formatted(pid, bid)

                num_program_statements = X.shape[1]
                fix_statements = fixed.get_fixes(pid, bid)

                # NNFL
                virtual_tests = np.identity(X.shape[1], dtype=np.single)
                m = models.SimpleFLNet(X.shape[1], 100)

                batch_size = 500
                inputs = torch.tensor(X)
                targets = torch.tensor(Y)
                dataset = TensorDataset(inputs, targets)
                data_loader = DataLoader(dataset, batch_size, shuffle=True)
                trn.train_fl(m, 1000, data_loader)
                nn_scores = m.forward(torch.tensor(virtual_tests)).detach().numpy().T
                all_ranks = rankdata(-nn_scores, method='average')
