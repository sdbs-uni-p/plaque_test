import math
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


if __name__ == "__main__":
    table = sys.argv[1]
    file1 = sys.argv[2]
    file2 = sys.argv[3]
    results_dir = sys.argv[4]

    with open(file1) as f1:
        entropies1 = pd.read_csv(f1, header=None)

    with open(file2) as f2:
        entropies2 = pd.read_csv(f2, header=None)

    # create dataframes from entropies
    df1 = pd.DataFrame(data=entropies1)
    df2 = pd.DataFrame(data=entropies2)

    # compare number of rows and columns
    if not df1.shape == df2.shape:
        raise Exception(f"different number of rows and/or columns in {file1} and {file2}")

    # append all columns in dataframes to list
    clmns1 = []
    clmns2 = []
    for i in range(0, len(df1.columns)):
        clmns1.extend(df1.iloc[:, i])
        clmns2.extend(df2.iloc[:, i])

    # collect entropy differences for all cells with entropy below 1
    entropy_diffs = [abs(clmns1[i] - clmns2[i]) for i in range(0, len(clmns1)) if clmns1[i] < 1 or clmns2[i] < 1]

    custom = {"grid.color": "black", "grid.linestyle": "-", "grid.linewidth": 0.5}
    sns.set_style("whitegrid", rc={
        'xtick.bottom': True,
        'ytick.left': True,
    })

    f, ax = plt.subplots(figsize=(8, 3))

    # create histplot from entropy_diffs
    print("Number of cells with entropy below 1:", len(entropy_diffs))
    max_entropy_diff = max(entropy_diffs)
    print("Maximal entropy difference:", round(max_entropy_diff, 3))
    binwidth = 0.005
    num_bins = math.ceil(max_entropy_diff / binwidth) + 1
    accs = [i * binwidth for i in range(num_bins)]
    for acc in accs:
        print(f"Number of cells with entropy difference {acc} or bigger:", sum(diff >= acc for diff in entropy_diffs))

    sns.histplot(data=entropy_diffs, bins=accs, color="g", ax=ax)
    sns.despine(ax=ax)
    ax.set(ylabel="", xlabel="Entropy difference")

    # show bar labels (counts)
    ax.bar_label(ax.containers[0])

    x_limit = binwidth * num_bins
    ax.set(xticks=accs + [x_limit])
    ax.set_xlim(0, x_limit)

    if not os.path.exists(f"{results_dir}/{table}"):
        os.makedirs(f"{results_dir}/{table}", exist_ok=True)

    f.text(0.00, 0.5, "Frequency", va='center', rotation='vertical')

    plt.savefig(f"{results_dir}/{table}/{table}_entropy_diffs_hist.pdf", bbox_inches='tight')
