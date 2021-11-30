import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def return_col_name(row, colnames):
    return colnames[np.argmin(row.values)]


def bests_to_counts(bests):
    counts = defaultdict(lambda : 0)
    for elem in bests:
        counts[elem] += 1
    return counts.keys(), counts.values()


if __name__=="__main__":
    df = pd.read_pickle("./EXAM.pkl")

    # Density EXAM
    sns.kdeplot(data=df, bw_method=.2)
    plt.xlabel("EXAM score")
    plt.xscale('log')
    plt.show()


    # PIE - for all the bugs, which technique performed the best with the lowest exam score
    df = df[df.columns[::-1]] # reverse df columns, ties should go to the simplier technique.. SBFL before NN etc
    pids = df.pop('pid')
    bids = df.pop('bid')
    bests = df.apply(lambda x: return_col_name(x, df.columns), axis=1)
    labels, counts = bests_to_counts(bests)
    print(labels, counts)
    plt.pie(counts, labels=labels, autopct='%1.1f%%', pctdistance=0.85)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.show()
