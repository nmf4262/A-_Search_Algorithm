import copy

class Node:
    def __init__(self, state, parent, action, cost, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.f() < other.f()
    
    def f(self):
        return self.cost + self.heuristic

def manhattan_distance(state, goal_state):
    """Calculates the Manhattan distance between two states."""
    distance = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                value = state[i][j][k]
                if value != 0:
                    goal_i, goal_j, goal_k = find_position(goal_state, value)
                    distance += abs(i - goal_i) + abs(j - goal_j) + abs(k - goal_k)
    return distance



def a_star_search(initial_state, goal_state):
    """Performs the A* search algorithm to find a solution."""
    
    frontier = {}
    visited = set()
    goal_state_tuple = tuple(tuple(tuple(inner) for inner in middle) for middle in goal_state)
    initial_state_tuple = tuple(tuple(tuple(inner) for inner in middle) for middle in initial_state)
    initial_node = Node(initial_state_tuple, None, None, 0, manhattan_distance(initial_state, goal_state))
    frontier[initial_state_tuple] = initial_node
    number_nodes = 1

    while frontier:
        state, node = min(frontier.items(), key=lambda x: x[1].f())
        del frontier[state]
        if state == goal_state_tuple:
            level, path, fs = find_level_path(node)
            return node, level, path, number_nodes, fs
        if state not in visited:
            visited.add(state)

            for action in ["E", "W", "N", "S", "U", "D"]:
                new_state = move(list(list(list(inner) for inner in middle) for middle in state), action)

                if new_state is not None:
                    number_nodes+=1
                    new_state_tuple = tuple(tuple(tuple(inner) for inner in middle) for middle in new_state)
                    new_node = Node(new_state_tuple, node, action, node.cost + 1, manhattan_distance(new_state, goal_state))
                    if new_state_tuple not in frontier or new_node.cost < frontier[new_state_tuple].cost:
                        frontier[new_state_tuple] = new_node

    return None

def find_level_path(node):
    level = 0
    path = []
    fs = []
    while node.parent:
        fs.append(str(node.f()))
        # print(node.state)
        # print(node.f())
        path.append(node.action)
        level += 1 
        node = node.parent
    if not node.parent:
        fs.append(str(node.f()))
    return level, path, fs



def move(state, action):
    """Moves the blank tile in the given direction."""
    blank_z, blank_y, blank_x = find_position(state, 0)

    if action == "E" and blank_x < 2:
        new_state = copy.deepcopy(state)
        new_state[blank_z][blank_y][blank_x] = new_state[blank_z][blank_y][blank_x + 1]
        new_state[blank_z][blank_y][blank_x + 1] = 0
        return new_state

    elif action == "W" and blank_x > 0:
        new_state = copy.deepcopy(state)
        new_state[blank_z][blank_y][blank_x] = new_state[blank_z][blank_y][blank_x - 1]
        new_state[blank_z][blank_y][blank_x - 1] = 0
        return new_state

    elif action == "N" and blank_y > 0:
        new_state = copy.deepcopy(state)
        new_state[blank_z][blank_y][blank_x] = new_state[blank_z][blank_y - 1][blank_x]
        new_state[blank_z][blank_y - 1][blank_x] = 0
        return new_state

    elif action == "S" and blank_y < 2:
        new_state = copy.deepcopy(state)
        new_state[blank_z][blank_y][blank_x] = new_state[blank_z][blank_y + 1][blank_x]
        new_state[blank_z][blank_y + 1][blank_x] = 0
        return new_state

    elif action == "U" and blank_z > 0:
        new_state = copy.deepcopy(state)
        new_state[blank_z][blank_y][blank_x] = new_state[blank_z - 1][blank_y][blank_x]
        new_state[blank_z - 1][blank_y][blank_x] = 0
        return new_state

    elif action == "D" and blank_z < 2:
        new_state = copy.deepcopy(state)
        new_state[blank_z][blank_y][blank_x] = new_state[blank_z + 1][blank_y][blank_x]
        new_state[blank_z + 1][blank_y][blank_x] = 0
        return new_state

def find_position(state, value):
    """Finds the position of the blank tile in the given state."""
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if state[i][j][k] == value:
                    return i, j, k
                



initial_state = [
[[1, 0, 3], [4, 2, 5], [6, 7, 8]],  
[[9, 10, 11], [12, 13, 14], [15, 16, 17]],
[[18, 19, 20], [21, 22, 23], [24, 25, 26]]
]

goal_state = [
    [[1, 2, 3],[4, 13, 5],[6, 7, 8]],
    [[9, 10, 11], [15, 12, 14], [24, 16, 17]],
    [[18, 19, 20], [21, 0, 23], [25, 22, 26]]
]

def read_puzzle(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    initial_state = []
    current_sublist = []

    for line in lines[:11]:
        if line.strip():
            # If the line is not empty, add its values to the current sublist
            current_sublist.append(list(map(int, line.strip().split())))
        else:
            # If the line is empty, start a new sublist
            initial_state.append(current_sublist)
            current_sublist = []

# Add the last sublist if there are remaining values
    if current_sublist:
        initial_state.append(current_sublist)


    current_sublist = []
    goal_state = []

    for line in lines[12:]:
        if line.strip():
            # If the line is not empty, add its values to the current sublist
            current_sublist.append(list(map(int, line.strip().split())))
        else:
            # If the line is empty, start a new sublist
            goal_state.append(current_sublist)
            current_sublist = []

    if current_sublist:
        goal_state.append(current_sublist)

    return initial_state, goal_state



def write_answer(file_path, depth_level_d, total_nodes_N, solution_actions, fs):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process lines 1 to 23 and append them to the output
    output_lines = lines[:23]

    # Add a blank line (line 24)
    output_lines.append("\n")

    # Replace the following placeholders with actual values obtained from your A* algorithm
    # f_values = [10, 15, 20, 25, 30, 35]  # Replace with the actual f(n) values
    solution_actions.reverse()
    fs.reverse()
    # Add the depth level (line 25)
    output_lines.append(f"\n{depth_level_d}\n")

    # Add the total number of nodes (line 26)
    output_lines.append(f"{total_nodes_N}\n")

    # Add the solution actions (line 27)
    output_lines.append('{'+" ".join(solution_actions) + "}\n")
    output_lines.append('{'+" ".join(fs) + "}\n")

    # Add the f values (line 28)
    # output_lines.append(" ".join(map(str, f_values)) + "\n")

    # Write the output to the output file
    output_file_path = "output.txt"  # Replace with your desired output file path
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(output_lines)




if __name__ == "__main__":
    file_path= 'Input3.txt'
    initial_states, goal_states = read_puzzle(file_path)
    node, level, path, number_nodes, fs = a_star_search(initial_states, goal_states)
    write_answer(file_path, level, number_nodes, path,fs)
