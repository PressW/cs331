import pandas as pd
import numpy as np



def set_state(filename):
    col_names = ['missionaries', 'cannibals', 'boat']
    start_df = pd.read_csv(filename, dtype=np.int32, header=None, names=col_names)
    start_df.index = ["left","right"]
    return start_df



def valid_successors(state):
    pass



start_state = set_state("test_start1.txt")
print("\n", start_state, "\n")
goal_state = set_state("test_goal1.txt")
print("\n", goal_state, "\n")

# print access index in dataframe
# print(goal_state.get_value("left","missionaries"), "\n")
