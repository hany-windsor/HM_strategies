import pandas as pd
import numpy as np
import itertools
from pathlib import Path
import json
import os


def converting_solver_solution_to_observation(df_solution_of_x, df_solution_of_y, total_cost, path_to_values):

    # Get unique feature values
    unique_features = df_solution_of_x['feature'].unique()

    # Create a list of all unique pairs of features
    feature_pairs = list(itertools.combinations(unique_features, 2))

    # Create an empty DataFrame to store the results1
    sequence_df = pd.DataFrame(index=[0])

    # Iterate through each pair of features and calculate the relationship
    for feature1, feature2 in feature_pairs:
        # Check if both features have a value of 1 in the original DataFrame
        has_feature1 = df_solution_of_x[(df_solution_of_x['feature'] == feature1) & (df_solution_of_x['value'] == 1)]
        has_feature2 = df_solution_of_x[(df_solution_of_x['feature'] == feature2) & (df_solution_of_x['value'] == 1)]

        if not has_feature1.empty and not has_feature2.empty:
            # Check if feature1 precedes feature2 by comparing their sequences
            if abs(has_feature1['sequence'].values[0] - has_feature2['sequence'].values[0]) == 1:
                if has_feature1['sequence'].values[0] < has_feature2['sequence'].values[0]:
                    sequence_df[f'platform_f{feature1}_precedes_f{feature2}'] = 1
                else:
                    sequence_df[f'platform_f{feature2}_precedes_f{feature1}'] = 1


    # Filter rows where value is 1
    filtered_df = df_solution_of_x[df_solution_of_x['value'] == 1]

    # Get unique feature values
    unique_features = filtered_df['feature'].unique()

    # Create a dictionary to store the setup values for each feature
    setup_dict = {f'p_f{feature}_setup': filtered_df[filtered_df['feature'] == feature]['setup'].values[0] for feature in
                  unique_features}

    # Create a DataFrame with one row using the setup_dict
    setups_df = pd.DataFrame([setup_dict])

    platform_res_df = pd.concat([sequence_df, setups_df], axis=1)

    path_to_platform_results_csv = Path(path_to_values,"platform_res_df.csv")
    platform_res_df.to_csv(path_to_platform_results_csv)


    #getting solution of y to the observation

    #getting unique set of vairiants

    set_of_variant = sorted(df_solution_of_y['variant'].unique())

    variant_res_df =pd.DataFrame()
    for variant in set_of_variant:
        filtered_solution_y_for_one_variant = df_solution_of_y[df_solution_of_y['variant'] == variant]
        df_variant_m = pd.DataFrame(filtered_solution_y_for_one_variant)

        # Get unique feature values
        unique_features = df_variant_m['feature'].unique()

        # Create a list of all unique pairs of features
        feature_pairs = list(itertools.combinations(unique_features, 2))

        # Create an empty DataFrame to store the results1
        sequence_df = pd.DataFrame(index=[0])

        # Iterate through each pair of features and calculate the relationship
        for feature1, feature2 in feature_pairs:
            # Check if both features have a value of 1 in the original DataFrame
            has_feature1 = df_variant_m[(df_variant_m['feature'] == feature1) & (df_variant_m['value'] == 1)]
            has_feature2 = df_variant_m[(df_variant_m['feature'] == feature2) & (df_variant_m['value'] == 1)]

            if not has_feature1.empty and not has_feature2.empty:
                # Check if feature1 precedes feature2 by comparing their sequences
                if abs(has_feature1['sequence'].values[0] - has_feature2['sequence'].values[0]) == 1:
                    if has_feature1['sequence'].values[0] < has_feature2['sequence'].values[0]:
                        sequence_df[f'v{variant}_f{feature1}_precedes_f{feature2}'] = 1
                    else:
                        sequence_df[f'v{variant}__f{feature2}_precedes_f{feature1}'] = 1

        # Filter rows where value is 1
        filtered_df = df_variant_m[df_variant_m['value'] == 1]

        # Get unique feature values
        unique_features = filtered_df['feature'].unique()

        # Create a dictionary to store the setup values for each feature
        setup_dict = {f'v{variant}_f{feature}_setup': filtered_df[filtered_df['feature'] == feature]['setup'].values[0] for feature in
                      unique_features}

        # Create a DataFrame with one row using the setup_dict
        setups_df = pd.DataFrame([setup_dict])

        variant_res_df = pd.concat([variant_res_df,sequence_df, setups_df], axis=1)

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

    folder_path =  r"C:\Users\enhan\PycharmProjects\strategiesHM\family_1_reduced"

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

    generated_data.to_csv("outputs/dataset_family_1_reduced.csv")
    generated_data.pop("total_cost")

    generated_data.to_csv("outputs/two_class_family_1_reduced.csv")


