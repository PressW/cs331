import pandas as pd
import numpy as np
import queue, sys, random



def set_state(filename):
    col_names = ['missionaries', 'cannibals', 'boat']
    start_df = pd.read_csv(filename, dtype=np.int32, header=None, names=col_names)
    start_df.index = ["left","right"]
    return start_df



def find_successors(passed_state, fringe, explored):
    state = None
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
        m1_state.set_value("right", "meta", state_to_string(state))
        m1_state.set_value("left", "meta", (state.get_value("left", "meta") + 1))
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
        m2_state.set_value("right", "meta", state_to_string(state))
        m2_state.set_value("left", "meta", (state.get_value("left", "meta") + 1))
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
        c1_state.set_value("right", "meta", state_to_string(state))
        c1_state.set_value("left", "meta", (state.get_value("left", "meta") + 1))
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
        m1c1_state.set_value("right", "meta", state_to_string(state))
        m1c1_state.set_value("left", "meta", (state.get_value("left", "meta") + 1))
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
        c2_state.set_value("right", "meta", state_to_string(state))
        c2_state.set_value("left", "meta", (state.get_value("left", "meta") + 1))
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
    # Playing with Stochasticity
    result = ((m + c) / 2) - random.uniform(0.00000, 0.001234)
    if result < 0: result = 0
    return result



def bfs(start, goal_file):
    # print("\nSTART STATE\n", start, "\n")
    fringe = queue.Queue()
    fringe.put(start)
    fringe_size = 1
    explored = {}
    explored[state_to_string(start)] = start
    start.set_value("left", "meta", int(1))
    while not fringe.empty():
        cur_state = fringe.get()
        explored[state_to_string(cur_state)] = cur_state
        if is_goal_state(cur_state, goal_file): return explored, fringe_size
        fringe_size += find_successors(cur_state, fringe, explored)



def dfs(start, goal_file):
    # print("\nSTART STATE\n", start, "\n")
    fringe = queue.LifoQueue()
    fringe.put(start)
    fringe_size = 1
    explored = {}
    explored[state_to_string(start)] = start
    start.set_value("left", "meta", int(1))
    while not fringe.empty():
        cur_state = fringe.get()
        explored[state_to_string(cur_state)] = cur_state
        if is_goal_state(cur_state, goal_file): return explored, fringe_size
        fringe_size += find_successors(cur_state, fringe, explored)



def iddfs(start, goal_file):
    # print("\nSTART STATE\n", start, "\n")
    max_depth = 1
    while max_depth < 100000:
        fringe = queue.LifoQueue()
        fringe.put(start)
        fringe_size = 0
        explored = {}
        explored[state_to_string(start)] = start
        start.set_value("left", "meta", int(1))
        while True:
            if fringe.empty(): break
            cur_state = fringe.get()
            depth = int(cur_state.get_value("left", "meta"))
            explored[state_to_string(cur_state)] = cur_state
            if is_goal_state(cur_state, goal_file): return explored, fringe_size
            if depth == max_depth: continue
            fringe_size += find_successors(cur_state, fringe, explored)
        max_depth += 1



def astar(start, goal_file):
    # print("\nSTART STATE\n", start, "\n")
    successors = queue.Queue()
    fringe = queue.PriorityQueue()
    explored = {}
    explored[state_to_string(start)] = start
    start.set_value("left", "meta", int(1))
    cost_so_far = {}
    fringe.put((0, start))
    fringe_size = 0
    cost_so_far[state_to_string(start)] = 0
    print(state_to_string(start), "\n")

    while not fringe.empty():
        cur_state = fringe.get()[1]
        find_successors(cur_state, successors, explored)
        for successor in successors.queue:
            cur_cost = cost_so_far[state_to_string(cur_state)] + 1
            if state_to_string(successor) not in cost_so_far or cur_cost < cost_so_far[state_to_string(successor)]:
                cost_so_far[state_to_string(successor)] = cur_cost
                priority = cur_cost + hueristic(successor, goal_file)
                successor.set_value("right", "meta", state_to_string(cur_state))
                fringe.put((priority, successor))
                fringe_size += 1
                explored[state_to_string(cur_state)] = cur_state
                if is_goal_state(cur_state, goal_file): return explored, fringe_size



def print_solution(q, q_name, cost, depth, output_file=False):
    if q.empty():
        print("\n", q_name, "is empty\n")
    else:
        if output_file is not False:
            with open(output_file, 'w') as of:
                for item in reversed(q.queue):
                    of.write(item.to_string())
                    of.write("\n\n")
                of.write("\nSPACE COMPLEXITY: {0}\n".format(cost))
                of.write("SOLUTION DEPTH: {0}\n".format(depth))
        for item in reversed(q.queue):
            print(item, "\n")
        print("\n")
        print("SPACE COMPLEXITY: ", cost)
        print("SOLUTION DEPTH: ", depth, "\n")



def calculate_solution(explored, start_file, goal_file):
    goal = set_state(goal_file)
    start = set_state(start_file)
    solution = queue.LifoQueue()
    goal_state = explored[state_to_string(goal)]
    start_state = explored[state_to_string(start)]
    key = state_to_string(goal_state)
    sol_depth = int(goal_state.get_value("left", "meta"))
    while key != state_to_string(start_state):
        cur_state = explored[key]
        par_key = str(cur_state.get_value("right", "meta")).split('.')[0]
        while len(par_key) < 6:
            par_key = "0" + par_key
        par_state = explored[par_key]
        solution.put(cur_state.drop("meta", 1))
        key = state_to_string(par_state)
    solution.put(start_state)
    return solution, sol_depth





if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("\nUSAGE ERROR")
        print("program_1.py <start_state_file> <goal_state_file> <search_mode> <output_file>\n")
    start = sys.argv[1]
    goal = sys.argv[2]
    mode = sys.argv[3]
    out_file = sys.argv[4]
    start_state = set_state(start)
    if mode == "bfs":
        explored, space_cost = bfs(start_state, goal)
    elif mode == "dfs":
        explored, space_cost = dfs(start_state, goal)
    elif mode == "iddfs":
        explored, space_cost = iddfs(start_state, goal)
    elif mode == "astar":
        explored, space_cost = astar(start_state, goal)
    else:
        print("\nMODE ERROR: Unsupported mode {0}".format(mode))
        sys.exit(0)
    solution_path, sol_depth = calculate_solution(explored, start, goal)
    print_solution(solution_path, "Solution path", space_cost, sol_depth, out_file)
