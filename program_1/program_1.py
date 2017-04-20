import pandas as pd
import numpy as np
import queue, sys



def set_state(filename):
    col_names = ['missionaries', 'cannibals', 'boat']
    start_df = pd.read_csv(filename, dtype=np.int32, header=None, names=col_names)
    start_df.index = ["left","right"]
    return start_df



def find_successors(passed_state, fringe, explored):
    if "parent" in passed_state:
        state = passed_state.drop("parent", 1)
    else:
        state = passed_state
    fringe_additions = 0

    # 1 missionary in the boat
    m1 = {"missionaries":  {"left": 1, "right": -1},
          "cannibals":     {"left": 0, "right": 0},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        m1_state = state.add(-1 * pd.DataFrame(m1))
    else:
        m1_state = state.add(pd.DataFrame(m1))
    if (valid_state(m1_state)) and (state_to_string(m1_state) not in explored):
        m1_state["parent"] = state_to_string(state)
        fringe.put(m1_state)
        fringe_additions += 1

    # 2 missionaries in the boat
    m2 = {"missionaries":  {"left": 2, "right": -2},
          "cannibals":     {"left": 0, "right": 0},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        m2_state = state.add(-1 * pd.DataFrame(m2))
    else:
        m2_state = state.add(pd.DataFrame(m2))
    if (valid_state(m2_state)) and (state_to_string(m2_state) not in explored):
        m2_state["parent"] = state_to_string(state)
        fringe.put(m2_state)
        fringe_additions += 1

    # 1 cannibal in the boat
    c1 = {"missionaries":  {"left": 0, "right": 0},
          "cannibals":     {"left": 1, "right": -1},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        c1_state = state.add(-1 * pd.DataFrame(c1))
    else:
        c1_state = state.add(pd.DataFrame(c1))
    if (valid_state(c1_state)) and (state_to_string(c1_state) not in explored):
        c1_state["parent"] = state_to_string(state)
        fringe.put(c1_state)
        fringe_additions += 1

    # 1 cannibal, 1 missionary in the boat
    m1c1 = {"missionaries":  {"left": 1, "right": -1},
          "cannibals":     {"left": 1, "right": -1},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        m1c1_state = state.add(-1 * pd.DataFrame(m1c1))
    else:
        m1c1_state = state.add(pd.DataFrame(m1c1))
    if (valid_state(m1c1_state)) and (state_to_string(m1c1_state) not in explored):
        m1c1_state["parent"] = state_to_string(state)
        fringe.put(m1c1_state)
        fringe_additions += 1

    # 2 cannibals in the boat
    c2 = {"missionaries":  {"left": 0, "right": 0},
          "cannibals":     {"left": 2, "right": -2},
          "boat":          {"left": 1, "right": -1}}
    if state.get_value("left", "boat") == 1:
        c2_state = state.add(-1 * pd.DataFrame(c2))
    else:
        c2_state = state.add(pd.DataFrame(c2))
    if (valid_state(c2_state)) and (state_to_string(c2_state) not in explored):
        c2_state["parent"] = state_to_string(state)
        fringe.put(c2_state)
        fringe_additions += 1

    return fringe_additions



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



def hueristic(state, goal_file):
    goal_state = set_state(goal_file)
    # Positive number indicate a movement from right bank to left bank, negative from left to right
    m = state.get_value("right", "missionaries") - goal_state.get_value("right", "missionaries")
    c = state.get_value("right", "cannibals")    - goal_state.get_value("right", "cannibals")
    return m + c



def bfs(start, goal_file):
    print("\nSTART STATE\n", start, "\n")
    fringe = queue.Queue()
    fringe.put(start)
    fringe_size = 0
    explored = {}
    explored[state_to_string(start)] = start
    while not fringe.empty():
        cur_state = fringe.get()
        print(hueristic(cur_state, "test_goal1.txt"))
        fringe_size += find_successors(cur_state, fringe, explored)
        explored[state_to_string(cur_state)] = cur_state
        if is_goal_state(cur_state, goal_file): return explored, fringe_size



def dfs(start, goal_file):
    print("\nSTART STATE\n", start, "\n")
    fringe = queue.LifoQueue()
    fringe.put(start)
    fringe_size = 0
    explored = {}
    explored[state_to_string(start)] = start
    while not fringe.empty():
        cur_state = fringe.get()
        fringe_size += find_successors(cur_state, fringe, explored)
        explored[state_to_string(cur_state)] = cur_state
        if is_goal_state(cur_state, goal_file): return explored, fringe_size



def iddfs(start, goal_file):
    print("\nSTART STATE\n", start, "\n")
    max_depth = 1
    while True:
        fringe = queue.LifoQueue()
        fringe.put(start)
        fringe_size = 0
        explored = {}
        explored[state_to_string(start)] = start
        while not fringe.empty():
            cur_state = fringe.get()
            if depth == max_depth: break
            fringe_size += find_successors(cur_state, fringe, explored)
            explored[state_to_string(cur_state)] = cur_state
            if is_goal_state(cur_state, goal_file): return explored, fringe_size
        max_depth += 1



def astar(start, goal_file):
    print("\nSTART STATE\n", start, "\n")
    successors = queue.Queue()
    fringe = queue.PriorityQueue()
    explored = {}
    cost_so_far = {}
    fringe.put((0, start))
    fringe_size = 0
    cost_so_far[state_to_string(start)] = 0

    while not fringe.empty():
        cur_state = fringe.get()[1]
        if is_goal_state(cur_state, goal_file): return explored, fringe_size
        fringe_size += find_successors(cur_state, successors, explored)
        for successor in successors.queue:
            cur_cost = cost_so_far[state_to_string(cur_state)] + 1
            if state_to_string(successor) not in cost_so_far or cur_cost < cost_so_far[state_to_string(successor)]:
                cost_so_far[state_to_string(successor)] = cur_cost
                priority = cur_cost + hueristic(successor, goal_file)
                successor["parent"] = state_to_string(cur_state)
                fringe.put((priority, successor))
                explored[state_to_string(cur_state)] = cur_state



def print_queue(q, q_name, output_file=False):
    if q.empty():
        print("\n", q_name, "is empty\n")
    else:
        if output_file is not False:
            with open(output_file, 'w') as of:
                for item in q.queue:
                    of.write(item.to_string())
                    of.write("\n\n")
        print("\n", q_name, "contents:\n")
        for item in q.queue:
            print(item)
        print("\n")



def calculate_cost(explored, start_file, goal_file, output_file):
    goal = set_state(goal_file)
    start = set_state(start_file)
    solution = queue.LifoQueue()
    goal_state = explored[state_to_string(goal)]
    start_state = explored[state_to_string(start)]
    key = state_to_string(goal_state)
    sol_depth = 0
    while key != state_to_string(start_state):
        cur_state = explored[key]
        par_state = explored[cur_state.get_value("right", "parent")]
        solution.put(cur_state.drop("parent", 1))
        key = state_to_string(par_state)
        sol_depth += 1
    solution.put(start_state)
    print_queue(solution, "Solution path", output_file)




if __name__ == "__main__":
    # if len(sys.argv) != 5:
    #     print("\nUSAGE ERROR")
    #     print("program_1.py <start_state_file> <goal_state_file> <search_mode> <output_file>\n")
    # start = sys.argv[1]
    # goal = sys.argv[2]
    # mode = sys.argv[3]
    # out_file = sys.argv[4]
    # if mode == "bfs":
    #     explored = bfs(start_state, goal)
    # elif mode == "dfs":
    #     explored = dfs(start_state, goal)
    # elif mode == "iddfs":
    #     explored = iddfs(start_state, goal)
    # elif mode == "astar":
    #     explored = astar(start_state, goal)
    # else:
    #     print("\nMODE ERROR: Unsupported mode {0}".format(mode))
    #     sys.exit(0)


    start_state = set_state("test_start1.txt")
    goal_state = set_state("test_goal1.txt")
    # fringe = queue.PriorityQueue()
    # fringe.put((12, start_state))
    # fringe.put((3, goal_state))
    # # while not fringe.empty():
    # #     item = fringe.get()
    # #     print("\n", item[1])
    # for item in fringe.queue:
    #     print(item[1])
    # # print_queue(fringe, "Fringe", "test.test")
    # while not fringe.empty():
    #     item = fringe.get()[1]
    #     print("\n", item)
    # for item in fringe.queue:
    #     print(item)
    # explored = bfs(start_state, "test_goal1.txt")
    # print_dict(explored, "test_start1.txt", "test_goal1.txt", "test.test")
