import pandas as pd
from itertools import product

# Define strategies for each FF
strategies = {
    "FF 1": [["PF 1"]],
    "FF 2": [["PF 2"]],
    "FF 3": [["PF 3"]],
    "FF 4": [["PF 4"], ["PF 5", "PF 6"]],
    "FF 5": [["PF 7"], ["PF 8", "PF 9"]],
    "FF 6": [["PF 10"]],
    "FF 7": [["PF 11"]],
    "FF 8": [["PF 12"]],
    "FF 9": [["PF 13"]],
    }

# Generate all combinations of strategies
all_combinations = list(product(*strategies.values()))

# List of all PFs
all_PF = [f"PF {i}" for i in range(1, 14)]

# Create an empty dataframe
df = pd.DataFrame(0, index=all_PF, columns=range(1, 5))

# Populate the dataframe
for col_num, combination in enumerate(all_combinations, start=1):
    for strategy in combination:
        for pf in strategy:
            df.at[pf, col_num] = 1



df.to_csv("strategies_family_1.csv")

