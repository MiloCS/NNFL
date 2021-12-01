import matplotlib.colors
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
    return counts


if __name__=="__main__":
    df = pd.read_pickle("./EXAM.pkl")
    colors = list(matplotlib.colors.TABLEAU_COLORS)[:len(df.columns) - 2]
    print(colors)

    # Density EXAM
    sns.kdeplot(data=df, bw_method=.2, palette=colors)
    plt.xlabel("EXAM score")
    plt.xscale('log')
    plt.show()


    # PIE - for all the bugs, which technique performed the best with the lowest exam score
    df_rev = df[df.columns[::-1]] # reverse df columns, ties should go to the simplier technique.. SBFL before NN etc
    pids = df_rev.pop('pid')
    bids = df_rev.pop('bid')
    bests = df_rev.apply(lambda x: return_col_name(x, df_rev.columns), axis=1)
    counts_dict = bests_to_counts(bests)
    labels = []
    counts = []
    for c in df.columns:
        if c != 'pid' and c != 'bid':
            labels.append(c)
            counts.append(counts_dict[c])

    print(labels, counts)
    plt.pie(counts, labels=labels, autopct='%1.1f%%', pctdistance=0.85, colors=colors)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.show()
