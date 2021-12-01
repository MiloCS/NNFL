import src.datasets.wash_fl as wash_fl
import src.datasets.fixed as fixed
import os
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from src.SBFL.sbfl.base import SBFL
from collections import defaultdict

import torch
from torch.utils.data import TensorDataset, DataLoader
import src.models as models
from src.classifiers.rbf import RBF
from src.classifiers.rbf import sigmoid
import src.train_util as trn


if __name__=="__main__":
    projects = ['Chart']    #, 'Closure', 'Lang', 'Math', 'Mockito', 'Time'

    EXAM_scores = defaultdict(lambda: [])
    pids = []
    bids = []

    for pid in projects:
        project_data_dir = 'data/fault-localization.cs.washington.edu/data/' + pid + '/'
        bug_ids = os.listdir(project_data_dir)
        for bid in bug_ids:
            if int(bid) < 1000:   # if real bug
                print(pid, bid)

                X, Y, n_lab, d_lab = wash_fl.data_formatted(pid, bid)

                num_program_statements = X.shape[1]
                fix_statements = fixed.get_fixes(pid, bid)

                # NNFL - SimpleFL
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

                fix_indexes = []
                for fix_point in fix_statements:
                    idx, = np.where(np.array(d_lab) == fix_point)
                    for elem in idx:
                        fix_indexes.append(elem)
                ranks = np.take(all_ranks, fix_indexes)

                if (len(ranks) > 0):  # TODO this should always be true but some bug is making it false sometimes
                    curr_EXAM = min(ranks) / num_program_statements
                    EXAM_scores['simpleFl'].append(curr_EXAM)

                # NNFL - SimpleFL-relu
                m = models.SimpleFLReluNet(X.shape[1], 100)
                trn.train_fl(m, 1000, data_loader)
                nn_scores = m.forward(torch.tensor(virtual_tests)).detach().numpy().T
                all_ranks = rankdata(-nn_scores, method='average')

                fix_indexes = []
                for fix_point in fix_statements:
                    idx, = np.where(np.array(d_lab) == fix_point)
                    for elem in idx:
                        fix_indexes.append(elem)
                ranks = np.take(all_ranks, fix_indexes)

                if (len(ranks) > 0):  # TODO this should always be true but some bug is making it false sometimes
                    curr_EXAM = min(ranks) / num_program_statements
                    EXAM_scores['simpleFl-relu'].append(curr_EXAM)

                # NNFL - RBF-sigmoid
                m = RBF(X.shape[1], 1, sigmoid)
                trn.train_fl(m, 1000, data_loader)
                nn_scores = m.forward(torch.tensor(virtual_tests)).detach().numpy().T
                all_ranks = rankdata(-nn_scores, method='average')

                fix_indexes = []
                for fix_point in fix_statements:
                    idx, = np.where(np.array(d_lab) == fix_point)
                    for elem in idx:
                        fix_indexes.append(elem)
                ranks = np.take(all_ranks, fix_indexes)

                if (len(ranks) > 0):  # TODO this should always be true but some bug is making it false sometimes
                    curr_EXAM = min(ranks) / num_program_statements
                    EXAM_scores['RBF-sigmoid'].append(curr_EXAM)

                # SBFL
                X = np.array(X, dtype=bool)
                Y = np.logical_not(np.array(Y, dtype=bool))     # SBFL assumes 1 is pass, 0 fail
                sbfl = SBFL(formula='Ochiai')
                sbfl.fit(X, Y)
                all_ranks = sbfl.ranks()


                fix_indexes = []
                for fix_point in fix_statements:
                    idx, = np.where(np.array(d_lab) == fix_point)
                    for elem in idx:
                        fix_indexes.append(elem)
                ranks = np.take(all_ranks, fix_indexes)

                if (len(ranks) > 0): # TODO this should always be true but some bug is making it false sometimes
                    curr_EXAM = min(ranks) / num_program_statements
                    EXAM_scores['sbfl-ochiai'].append(curr_EXAM)
                    pids.append(pid)
                    bids.append(bid)

    df = pd.DataFrame.from_dict(EXAM_scores)
    df = df.assign(pid=pids)
    df = df.assign(bid=bids)
    df.to_pickle("./EXAM.pkl")
