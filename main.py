import src.d4j_util as d4j
import src.config as cf
import src.datasets.d4j_fl as d4j_fl
import src.models as models
import src.train_util as trn
#from src.SBFL.sbfl.base import SBFL

import psycopg2
import numpy as np
import math
import torch
from torch.utils.data import TensorDataset, DataLoader

if __name__ == '__main__':
    # We're going to build a FL NN for a specific bug.
    project = "Mockito"
    bug_id = "10"

    #res = d4j.get_modified_classes_info("Mockito", "10")
    #print("Classes Modified in Fix", res)

    # ideally, we want to fault localize at a line level, but we need to extract the modified line information from the git log in the 'b' and 'f' versions of the bug and diff'ing the logs

    # get all test_id's for a specific bug, the fl dataset only has test runs for the 'b' versions
    full_project_name = project + '_' + bug_id + 'b'
    with psycopg2.connect(cf.c_str) as conn:
        with conn.cursor() as cur:
            tests = d4j_fl.get_all_tests(cur, full_project_name)
            print("Num Tests", len(tests))

            X, Y, n_lab, d_lab = d4j_fl.data_formatted(cur, full_project_name)
            # 2d np.array uint, 2d np.array uint, list of row labels, list of col labels
            # Y; 0=pass, 1=fail
            print(X.shape, Y.shape)

            # this step is optional; we may want to investigate the model difference between using the line 'count' or just the line 'binary' as input
            X = np.minimum(X, 1)
            virtual_tests = np.identity(X.shape[1], dtype=np.single)

            # we then train a NN to learn execution result from the coverages
            m = models.SimpleFLNet(X.shape[1], 100)

            batch_size = 500
            inputs = torch.tensor(X)
            targets = torch.tensor(Y)

            dataset = TensorDataset(inputs, targets)
            data_loader = DataLoader(dataset, batch_size, shuffle=True)

            nn_suspicion_scores_before_trn = m.forward(torch.tensor(virtual_tests))
            trn.train_fl(m, 1000, data_loader)


            # once the NN is trained, its pretty easy to extract the suspicion scores using 'virtual tests cases'
            nn_suspicion_scores = m.forward(torch.tensor(virtual_tests))
            # we can then compare this to SB-FL Ochai

            X = np.array(X, dtype=bool)
            Y = np.array(Y, dtype=bool)
            sbfl_suspicion_scores = []
            sbfl = SBFL(formula='Ochiai')
            sbfl.fit(X, Y)
            # print(sbfl.ranks(method='max'))
            sbfl_suspicion_scores = sbfl.to_frame()['score']

            # it might be interesting to investigation the correlation, i'd expect some non trivial positive value after training
            print('sbfl/nn localization correlation coef before:', np.corrcoef(nn_suspicion_scores_before_trn.detach().numpy().T, np.array(sbfl_suspicion_scores)))
            print('sbfl/nn localization correlation coef after:', np.corrcoef(nn_suspicion_scores.detach().numpy().T, np.array(sbfl_suspicion_scores)))








