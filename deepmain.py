import src.datasets.wash_fl as wash_fl
import src.datasets.fixed as fixed
import os, sys
import numpy as np
from scipy.stats import rankdata
from src.SBFL.sbfl.base import SBFL

import torch
from torch.utils.data import TensorDataset, DataLoader
import src.models as models
from src.deep import FLFeatureNet
import src.train_util as trn
import src.features as feat

np.set_printoptions(threshold=sys.maxsize)


if __name__=="__main__":
    projects = ['Chart']    #, 'Closure', 'Lang', 'Math', 'Mockito', 'Time'

    for pid in projects:
        project_data_dir = 'data/fault-localization.cs.washington.edu/data/' + pid + '/'
        bug_ids = os.listdir(project_data_dir)
        sbfl_data = None
        complex_data = None
        for bid in bug_ids:
            if int(bid) < 1000:   # if real bug
                print(pid, bid)

                X, Y, n_lab, d_lab = wash_fl.data_formatted(pid, bid)

                num_program_statements = X.shape[1]
                fix_statements = fixed.get_fixes(pid, bid)

                # NNFL
                Y = Y.astype(np.int64).squeeze()
                if (len(Y.shape) != 0 and len(X.shape) != 0):
                #virtual_tests = np.identity(X.shape[1], dtype=np.single)
                    # f = feat.get_spectrum_features(X, Y)
                    # print(f.shape)
                    # if sbfl_data is None:
                    #     sbfl_data = f
                    # else:
                    #     sbfl_data = np.hstack((sbfl_data, f))

                    c = feat.get_complexity_features(d_lab, pid, bid)
                    print(c.shape)
                    if complex_data is None:
                        complex_data = c
                    else:
                        complex_data = np.hstack((sbfl_data, c))
        #sbfl_data[~np.isfinite(total_data)] = 0
        #print(sbfl_data.shape)
        np.savez("tmp/complex.npz", complex_data=complex_data)

       # print(sbfl_data[:, 0:20])
                # m = FLFeatureNet(X.shape[1], 100)

                # batch_size = 500
                # inputs = torch.tensor(X)
                # targets = torch.tensor(Y)
                # dataset = TensorDataset(inputs, targets)
                # data_loader = DataLoader(dataset, batch_size, shuffle=True)
                # trn.train_fl(m, 1000, data_loader)
                # nn_scores = m.forward(torch.tensor(virtual_tests)).detach().numpy().T
                # all_ranks = rankdata(-nn_scores, method='average')
