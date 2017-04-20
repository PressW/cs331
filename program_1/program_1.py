import pandas as pd
import numpy as np
import queue



q = queue.Queue()



def set_state(filename):
    col_names = ['missionaries', 'cannibals', 'boat']
    start_df = pd.read_csv(filename, dtype=np.int32, header=None, names=col_names)
    start_df.index = ["left","right"]
    return start_df



def find_successors(state, fringe, explored):
    # 1 missionary in the boat
    m1 = {"missionaries":  {"left": 1, "right": -1},
          "cannibals":     {"left": 0, "right": 0},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        m1_state = state.add(-1 * pd.DataFrame(m1))
    else:
        m1_state = state.add(pd.DataFrame(m1))
    if (valid_state(m1_state)) and (state_to_string(m1_state) not in explored):
        fringe.put(m1_state)

    # 2 missionaries in the boat
    m2 = {"missionaries":  {"left": 2, "right": -2},
          "cannibals":     {"left": 0, "right": 0},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        m2_state = state.add(-1 * pd.DataFrame(m2))
    else:
        m2_state = state.add(pd.DataFrame(m2))
    if (valid_state(m2_state)) and (state_to_string(m2_state) not in explored):
        fringe.put(m2_state)

    # 1 cannibal in the boat
    c1 = {"missionaries":  {"left": 0, "right": 0},
          "cannibals":     {"left": 1, "right": -1},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        c1_state = state.add(-1 * pd.DataFrame(c1))
    else:
        c1_state = state.add(pd.DataFrame(c1))
    if (valid_state(c1_state)) and (state_to_string(c1_state) not in explored):
        fringe.put(c1_state)

    # 1 cannibal, 1 missionary in the boat
    m1c1 = {"missionaries":  {"left": 1, "right": -1},
          "cannibals":     {"left": 1, "right": -1},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        m1c1_state = state.add(-1 * pd.DataFrame(m1c1))
    else:
        m1c1_state = state.add(pd.DataFrame(m1c1))
    if (valid_state(m1c1_state)) and (state_to_string(m1c1_state) not in explored):
        fringe.put(m1c1_state)

    # 2 cannibals in the boat
    c2 = {"missionaries":  {"left": 0, "right": 0},
          "cannibals":     {"left": 2, "right": -2},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        c2_state = state.add(-1 * pd.DataFrame(c2))
    else:
        c2_state = state.add(pd.DataFrame(c2))
    if (valid_state(c2_state)) and (state_to_string(c2_state) not in explored):
        fringe.put(c2_state)



def valid_state(state):
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
    return valid


def is_goal_state(state, goal_file):
    goal_state = set_state(goal_file)
    if state.get_value("left", "missionaries")  != goal_state.get_value("left", "missionaries"):  return False
    if state.get_value("left", "cannibals")     != goal_state.get_value("left", "cannibals"):     return False
    if state.get_value("left", "boat")          != goal_state.get_value("left", "boat"):          return False
    if state.get_value("right", "missionaries") != goal_state.get_value("right", "missionaries"): return False
    if state.get_value("right", "cannibals")    != goal_state.get_value("right", "cannibals"):    return False
    if state.get_value("right", "boat")         != goal_state.get_value("right", "boat"):         return False
    return True



def state_to_string(state):
    return str(state.get_value("left", "missionaries"))  + str(state.get_value("left", "cannibals"))  + str(state.get_value("left", "boat")) + \
           str(state.get_value("right", "missionaries")) + str(state.get_value("right", "cannibals")) + str(state.get_value("right", "boat"))



def bfs(start, goal_file):
    print("\nSTART STATE\n", start, "\n")
    fringe = queue.Queue()
    fringe.put(start)
    explored = {}
    explored[state_to_string(start)] = start
    while not fringe.empty():
        cur_state = fringe.get()
        find_successors(cur_state, fringe, explored)
        explored[state_to_string(cur_state)] = cur_state
        if is_goal_state(cur_state, goal_file): return explored



def print_queue(q, q_name):
    if q.empty():
        print("\n", q_name, "is empty\n")
    else:
        print("\n", q_name, "contents:\n")
        while not q.empty():
            print(q.get())
        print("\n")



def print_dict(explored):
    print("\nExplored contents:\n")
    for key in explored:
        # print("\n", key)s
        print(explored[key], "\n")



if __name__ == "__main__":
    start_state = set_state("test_start1.txt")
    explored = bfs(start_state, "test_goal1.txt")
    print_dict(explored)
