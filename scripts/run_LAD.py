import os

import pandas as pd

from sklearn.model_selection import train_test_split

#read data

csv_file_path = "outputs/two_class_family_2_reduced.csv"

# Create a DataFrame from the CSV file
data = pd.read_csv(csv_file_path)
data = data.iloc[:, 1:]

# Split the data into 80% training and 20% testing
train_df, test_df = train_test_split(data, test_size=0.2, random_state=100)


# Save the training and testing DataFrames into separate CSV files
#train_df.to_csv('training_data.csv', index=False)
#test_df.to_csv("testing_data.csv", header=False, index=False)

test_df.to_csv("testing_data.txt", sep='\t', header=False, index=False)

heading_row = [3] * len(train_df.columns)

# Use loc to insert the new row after the column name row
train_df.loc[-1] = heading_row
train_df.index = train_df.index + 1
train_df.sort_index(inplace=True)

train_df.to_csv(r'C:\cbmLAD\raw data.txt', sep='\t', index=False)
test_df.to_csv(r'C:\cbmLAD\test data.txt', sep='\t', header=False, index=False)


#os.startfile(r"C:\Users\enhan\OneDrive\Documents\Visual Studio 2017\Projects\CBM-LAD Aug 2018\CBM-LAD Aug 2018\Executable files\CBM_LAD_One Vs All _ Max Hamming _ Aug 2018.exe")
os.startfile(r"C:\cbmLAD\CBM_LAD_One Vs One _ Random _ Aug 2018.exe")
#os.startfile(r"C:\cbmLAD\Testing Multi-Class.exe")

"C:\cbmLAD\CBM_LAD_One Vs One _ Random _ Aug 2018.exe"