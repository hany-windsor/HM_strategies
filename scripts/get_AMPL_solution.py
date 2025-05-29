#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd
from pathlib import Path
from amplpy import AMPL, Environment
import json
import random
import solver_solution_to_observation

ampl = AMPL(Environment(r'C:/bin'))

def main(argc, argv):


    #os.chdir(os.path.dirname(__file__) or os.curdir)

    ampl.set_option("solver", "cplex")
    #ampl.setOption('gurobi_options', 'timelim=400')

    #ampl.setOption('cplex_options','poolstub savesol')
    #ampl.setOption('cplex_options', 'parallelmode=-1')


    if argc > 1:
        ampl.set_option("solver", argv[1])

    ampl.read("C:/bin/lin_strategies.mod")
    ampl.read_data("C:/bin/family_3.txt")

    for i in range(11):
        random_num = int(round((random.uniform(0, 1000)), 0))
        ampl.setOption("cplex_options", f"poolstub savesol mipsearch = 2 nodesel = 3 seed={random_num} timelimit=7200")
        #ampl.setOption('gurobi_options', 'timelim=650')
        #ampl.setOption('gurobi_options', 'solutionstub = 12')
        #ampl.setOption('gurobi_options', 'PoolSolutions=50')
        #ampl.setOption('gurobi_options', 'ams_stub=allopt ams_mode=2')

        # Create the folder if it doesn't exist
        #os.makedirs(folder_name, exist_ok=True)

        # Define the file path for the CSV file within the folder
        file_name_x = f'values_var_x.csv'
        file_name_y = f'values_var_y.csv'
        file_name_obj_fun = f'values_var_z.json'
        file_name_epsilon = f'values_var_epsilon.csv'

        ampl.solve()

        for sol in range(1, ampl.get_value("cost.npool") + 1):
            folder_name = f'family_3/outputs{i}_{sol}'

            os.makedirs(folder_name, exist_ok=True)
            ampl.eval(f"solution savesol{sol}.sol;")  # load the solution

            data_epsilon = ampl.get_data(r"epsilon").to_dict()  # store the value of variable x
            epsilon_df = pd.DataFrame(data_epsilon.items(), columns=['Key', "value"])
            epsilon_df[["strategy"]] = pd.DataFrame(epsilon_df['Key'].tolist())
            epsilon_df = epsilon_df.drop(columns=['Key'])
            path_to_epsilon_values_csv = Path(folder_name) / file_name_epsilon
            epsilon_df.to_csv(path_to_epsilon_values_csv)


            data_x = ampl.get_data(r"x").to_dict()  # store the value of variable x
            x_df = pd.DataFrame(data_x.items(), columns=['Key', "value"])
            x_df[["feature", "sequence", "setup"]] = pd.DataFrame(x_df['Key'].tolist())
            x_df = x_df.drop(columns=['Key'])
            path_to_x_values_csv = Path(folder_name) / file_name_x
            x_df.to_csv(path_to_x_values_csv)

            data_y = ampl.get_data(r"y").to_dict()  # store the value of variable x
            y_df = pd.DataFrame(data_y.items(), columns=['Key', "value"])
            y_df[["feature", "variant", "sequence", "setup"]] = pd.DataFrame(y_df['Key'].tolist())
            y_df = y_df.drop(columns=['Key'])
            path_to_y_values_csv = Path(folder_name) / file_name_y
            y_df.to_csv(path_to_y_values_csv)

            data_obj = ampl.get_objective("cost").get_values().to_pandas()  # store the value of variable x

            objective_value = {'total_cost': data_obj.loc[0, "cost"]}
            path_obj_fun = Path(folder_name) / file_name_obj_fun

            # # Save the dictionary as a JSON file
            with open(path_obj_fun, 'w') as json_file:
                json.dump(objective_value, json_file, indent=2)

        solve_result = ampl.get_value("solve_result")
        if solve_result != "solved":
            raise Exception("Failed to solve (solve_result: {})".format(solve_result))



if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
