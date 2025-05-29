import pandas as pd
from itertools import product

# Define strategies for each FF
strategies = {
    "FF 1": [["PF 1"]],
    "FF 2": [["PF 2"]],
    "FF 3": [["PF 3"]],
    "FF 4": [["PF 4"]],
    "FF 5": [["PF 5"]],
    "FF 6": [["PF 6"]],
    "FF 7": [["PF 7"]],
    "FF 8": [["PF 8"]],
    "FF 9": [["PF 9"]],
    "FF 10": [["PF 10"]],
    "FF 11": [["PF 11"]],
    "FF 12": [["PF 12"]],
    "FF 13": [["PF 13"]],
    "FF 14": [["PF 14"]],
    "FF 15": [["PF 15"]],
    "FF 16": [["PF 16"]],
    "FF 17": [["PF 17"]],
    "FF 18": [["PF 18"]],
    "FF 19": [["PF 19"]],
    "FF 20": [["PF 20"]],
    "FF 21": [["PF 21"]],
    "FF 22": [["PF 22"]],
    "FF 23": [["PF 23"]],
    "FF 24": [["PF 24"]],
    "FF 25": [["PF 25"], ["PF 26", "PF 27"]],
    "FF 26": [["PF 28"], ["PF 29", "PF 30"]],
    "FF 27": [["PF 31"], ["PF 32", "PF 33"]],
    "FF 28": [["PF 34"], ["PF 35", "PF 36"]],
    "FF 29": [["PF 37"], ["PF 38", "PF 39"]],
    "FF 30": [["PF 40"], ["PF 41", "PF 42"]],
    "FF 31": [["PF 43"]],
    "FF 32": [["PF 44"]],
    "FF 33": [["PF 45"], ["PF 46", "PF 47"]],
    "FF 34": [["PF 48"], ["PF 49", "PF 50"]],
}

# Generate all combinations of strategies
all_combinations = list(product(*strategies.values()))

# List of all PFs
all_PF = [f"PF {i}" for i in range(1, 51)]

# Create an empty dataframe
df = pd.DataFrame(0, index=all_PF, columns=range(1, 257))

# Populate the dataframe
for col_num, combination in enumerate(all_combinations, start=1):
    for strategy in combination:
        for pf in strategy:
            df.at[pf, col_num] = 1



df.to_csv("strategies_family_2.csv")

