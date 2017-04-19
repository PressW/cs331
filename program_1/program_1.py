import pandas as pd
import numpy as np
import queue


q = queue.Queue()



def set_state(filename):
    col_names = ['missionaries', 'cannibals', 'boat']
    start_df = pd.read_csv(filename, dtype=np.int32, header=None, names=col_names)
    start_df.index = ["left","right"]
    return start_df



def find_successors(state):
    valid_successors = []
    
    # 1 missionary in the boat
    m1 = {"missionaries":  {"left": 1, "right": -1},
          "cannibals":     {"left": 0, "right": 0},
          "boat":          {"left": 1, "right": -1}}
    m1_state = state.add(pd.DataFrame(m1))
    if (valid_state(m1_state)):
        valid_successors.append(m1_state)
        q.put(m1_state)
#    print("\n1 missionary in the boat\n", m1_state)

    # 2 missionaries in the boat
    m2 = {"missionaries":  {"left": 2, "right": -2},
          "cannibals":     {"left": 0, "right": 0},
          "boat":          {"left": 1, "right": -1}}
    m2_state = state.add(pd.DataFrame(m2))
    if (valid_state(m2_state)):
        valid_successors.append(m2_state)
        q.put(m2_state)
#    print("\n2 missionaries in the boat\n", m2_state)

    # 1 cannibal in the boat
    c1 = {"missionaries":  {"left": 0, "right": 0},
          "cannibals":     {"left": 1, "right": -1},
          "boat":          {"left": 1, "right": -1}}
    c1_state = state.add(pd.DataFrame(c1))
    if (valid_state(c1_state)):
        valid_successors.append(c1_state)
        q.put(c1_state)
#    print("\n1 cannibal in the boat\n", c1_state)

    # 1 cannibal, 1 missionary in the boat
    m1c1 = {"missionaries":  {"left": 1, "right": -1},
          "cannibals":     {"left": 1, "right": -1},
          "boat":          {"left": 1, "right": -1}}
    m1c1_state = state.add(pd.DataFrame(m1c1))
    if (valid_state(m1c1_state)):
        valid_successors.append(m1c1_state)
        q.put(m1c1_state)
#    print("\n1 missionary, 1 cannibal in the boat\n", m1c1_state)

    # 2 cannibals in the boat
    c2 = {"missionaries":  {"left": 0, "right": 0},
          "cannibals":     {"left": 2, "right": -2},
          "boat":          {"left": 1, "right": -1}}
    c2_state = state.add(pd.DataFrame(c2))
    if (valid_state(c2_state)):
        valid_successors.append(c2_state)
        q.put(c2_state)
#    print("\n2 cannibals in the boat\n", c2_state)

    return valid_successors



def valid_state(state):
#    print("\nmissionaries right = " , state.get_value("right", "missionaries"))
#    print("cannibals right = "     , state.get_value("right", "cannibals"))
#    print("missionaries left = "  , state.get_value("left",  "missionaries"))
#    print("cannibals left = "      , state.get_value("left",  "cannibals"))

    valid = True
    if state.get_value("right", "missionaries") < 0 or state.get_value("left", "missionaries") < 0 or \
       state.get_value("right", "cannibals") < 0    or state.get_value("left", "cannibals") < 0 or \
       state.get_value("right", "boat") < 0         or state.get_value("left", "boat") < 0:
        valid = False
    if state.get_value("right", "missionaries") != 0:
        if state.get_value("right", "missionaries") < state.get_value("right", "cannibals"):
            valid = False
    if state.get_value("left", "missionaries") != 0:
        if state.get_value("left", "missionaries") < state.get_value("left", "cannibals"):
            valid = False
#    print("Valid: ", valid)
    return valid



start_state = set_state("test_start1.txt")
successors = find_successors(start_state)
print("\n", successors, "\n")
valid_state(start_df)
while not q.empty():
    print(q.get())

print("\n", start_state, "\n")
goal_state = set_state("test_goal1.txt")
print("\n", goal_state, "\n")

# print access index in dataframe
# print(goal_state.get_value("left","missionaries"), "\n")
