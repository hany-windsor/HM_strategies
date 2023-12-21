import pandas as pd
import numpy as np
import itertools
from pathlib import Path
import json
import os


def converting_solver_solution_to_observation(df_solution_of_x, df_solution_of_y, total_cost, path_to_values):
    # Filter the DataFrame to keep rows where Value is 1
    filtered_df = df_solution_of_x[df_solution_of_x['value'] == 1]

    # Sort the DataFrame by Sequence in ascending order
    sorted_df = filtered_df.sort_values(by='sequence')

    # Create a new DataFrame with one row and unique Sequence values as columns
    sequence_df = pd.DataFrame(columns=sorted_df['sequence'].unique())

    # Set the feature numbers for each sequence value in the new DataFrame
    sequence_df.loc[0] = [
        sorted_df[sorted_df['sequence'] == seq]['feature'].values[0] if seq in sorted_df['sequence'].values else 0 for
        seq in sequence_df.columns]

    # Rename the columns by adding "platform" to their names
    sequence_df.columns = ['P_S' + str(col) for col in sequence_df.columns]


    # Filter rows where value is 1
    filtered_df = df_solution_of_x[df_solution_of_x['value'] == 1]

    # Get unique feature values
    unique_features = filtered_df['feature'].unique()

    # Create a dictionary to store the setup values for each feature
    setup_dict = {f'P_f{feature}_setup': filtered_df[filtered_df['feature'] == feature]['setup'].values[0] for feature in
                  unique_features}

    # Create a DataFrame with one row using the setup_dict
    setups_df = pd.DataFrame([setup_dict])

    platform_res_df = pd.concat([sequence_df, setups_df], axis=1)

    path_to_platform_results_csv = Path(path_to_values,"platform_res_df.csv")
    platform_res_df.to_csv(path_to_platform_results_csv)


    #getting solution of y to the observation

    # Filter the DataFrame to keep rows where Value is 1
    filtered_df = df_solution_of_y[df_solution_of_y['value'] == 1]

    # Sort the DataFrame by Variant and Sequence in ascending order
    sorted_df = filtered_df.sort_values(by=['variant', 'sequence'])

    # Get unique Variant and Sequence numbers
    unique_variants = sorted_df['variant'].unique()
    unique_sequences = sorted_df['sequence'].unique()
    unique_features = filtered_df['feature'].unique()

    # Create an empty dictionary to store the results
    sequence_dic = {}
    setup_dict = {}


    # Iterate over variant numbers
    for variant in unique_variants:
        # Iterate over sequence numbers
        for sequence in unique_sequences:
            # Filter the DataFrame for the current variant and sequence
            feature_values = sorted_df[
                (sorted_df['variant'] == variant) & (sorted_df['sequence'] == sequence)
                ]['feature'].values
            if feature_values.any():
                sequence_dic[f'V{variant}_S{sequence}'] = feature_values[0]
                setup_dict [f'V{variant}_f{feature_values[0]}_setup'] = sorted_df.iloc[0]['setup']
            else:
                sequence_dic[f'V{variant}_S{sequence}'] = 0
    # Create the final DataFrame with a single row
    sequence_df = pd.DataFrame([sequence_dic])
    setups_df = pd.DataFrame([setup_dict])

    #Get unique feature values


    # Create a dictionary to store the setup values for each feature


    # Create a DataFrame with one row using the setup_dict


    variant_res_df = pd.concat([sequence_df, setups_df], axis=1)

    path_to_variant_results_csv = Path(path_to_values,"variant_res_df.csv")
    variant_res_df.to_csv(path_to_variant_results_csv)

    full_solution = pd.concat([platform_res_df, variant_res_df, total_cost], axis=1)


    path_to_full_solution_csv = Path(path_to_values,"full_sol_df.csv")
    full_solution.to_csv(path_to_full_solution_csv)
    return full_solution


if __name__ == "__main__":

    generated_data= pd.DataFrame()
    file_name_x = f'values_var_x.csv'
    file_name_y = f'values_var_y.csv'
    file_name_obj_fun = f'values_var_z.json'

    folder_path =  r"C:\Users\enhan\PycharmProjects\strategiesHM\family_2_reduced"

    # Get a list of subfolder names
    subfolder_names = [subfolder for subfolder in os.listdir(folder_path) if
                       os.path.isdir(os.path.join(folder_path, subfolder))]

    for solution in subfolder_names:
        folder_name = solution

        path_to_values= Path(folder_path,folder_name)
        full_path_x = os.path.join(path_to_values, file_name_x)
        full_path_y = os.path.join(path_to_values, file_name_y)
        full_path_obj_fun = os.path.join(path_to_values, file_name_obj_fun)

        path_to_values_var_x_csv = Path(full_path_x)
        values_var_x = pd.read_csv(path_to_values_var_x_csv)
        path_to_values_var_y_csv = Path(full_path_y)
        values_var_y = pd.read_csv(path_to_values_var_y_csv)


        # Read the JSON file
        with open(full_path_obj_fun, 'r') as json_file:
            objective_value = json.load(json_file)

        cost = {
            "total_cost": [objective_value['total_cost']]
        }

        # Convert the dictionary to a DataFrame
        total_cost = pd.DataFrame(cost)

        one_observation = converting_solver_solution_to_observation(values_var_x, values_var_y, total_cost, path_to_values)
        generated_data = pd.concat([generated_data, one_observation], ignore_index=True)
        generated_data = generated_data.fillna(0)

        total_cost_column = generated_data.pop("total_cost")  # Remove the "total_cost" column from the DataFrame
        generated_data.insert(0, "total_cost", total_cost_column)  # Insert it as the first column


        #drop duplication
        #generated_data = generated_data.drop_duplicates()

        percentile_25 = np.percentile(generated_data['total_cost'], 25)

        # Create the 'class' column based on the condition
        generated_data['class'] = np.where(generated_data['total_cost'] > percentile_25, 0, 1)
        class_column = generated_data.pop("class")  # Remove the "total_cost" column from the DataFrame
        generated_data.insert(0, "class", class_column)  # Insert it as the first column

        # Iterate through each column and check if all values in the column are the same
        for column in generated_data.columns:
            if len(generated_data[column].unique()) == 1:
                # Drop the column if all values are the same
                generated_data.drop(column, axis=1, inplace=True)

    generated_data.to_csv("outputs/dataset_family_2_reduced.csv")
    generated_data.pop("total_cost")

    generated_data.to_csv("outputs/two_class_family_2_reduced.csv")


