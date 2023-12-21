import pandas as pd
from itertools import combinations

# Load your CSV data
csv_file_path = "outputs/two_class_family_1_reduced.csv"
data = pd.read_csv(csv_file_path)
data = data.iloc[:, 1:]

# Calculate the number of rows per partition
num_rows = len(data)
partition_size = num_rows // 5

# Split the data into 5 almost equal partitions
partitions = [data[i * partition_size:(i + 1) * partition_size] for i in range(5)]

# Generate combinations of 4 training partitions and 1 testing partition
combinations = list(combinations(range(5), 4))

# Create and save the training and testing sets
for i, combination in enumerate(combinations):
    training_set = pd.concat([partitions[j] for j in combination])
    testing_set = partitions[list(set(range(5)) - set(combination))[0]]

    # Save the training and testing sets to separate CSV files
    training_set.to_csv(f'training_set_{i + 1}.csv', index=False)
    testing_set.to_csv(f'testing_set_{i + 1}.csv', index=False)
