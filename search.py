import queue
import copy

# A node represents a specific state and its corresponding details within the search tree created.
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
# The heuristic function used is the manhattan distance, returns the total of all the manhattan distances of the tiles.
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
# Returns the new state after an action is performed on the current state.
def move(state, action):
    empty_z, empty_y, empty_x = find_position(state, 0)

    if action == "U" and empty_z > 0:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z - 1][empty_y][empty_x]
        new_state[empty_z - 1][empty_y][empty_x] = 0
        return new_state

    elif action == "D" and empty_z < 2:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z + 1][empty_y][empty_x]
        new_state[empty_z + 1][empty_y][empty_x] = 0
        return new_state
    
    elif action == "N" and empty_y > 0:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y - 1][empty_x]
        new_state[empty_z][empty_y - 1][empty_x] = 0
        return new_state

    elif action == "S" and empty_y < 2:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y + 1][empty_x]
        new_state[empty_z][empty_y + 1][empty_x] = 0
        return new_state
    
    elif action == "W" and empty_x > 0:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y][empty_x - 1]
        new_state[empty_z][empty_y][empty_x - 1] = 0
        return new_state

    elif action == "E" and empty_x < 2:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y][empty_x + 1]
        new_state[empty_z][empty_y][empty_x + 1] = 0
        return new_state
# Returns the position of a specific value within a state.
def find_position(state, value):
    """Finds the position of the blank tile in the given state."""
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if state[i][j][k] == value:
                    return i, j, k
# Performs the A* search algorithm and returns the optimal goal node.
def a_star_search(initial_state, goal_state):
    """Performs the A* search algorithm to find a solution to the 26-puzzle problem."""

    frontier = queue.PriorityQueue()
    visited = []
    total_nodes = 0

    frontier.put(Node(initial_state, None, None, 0, manhattan_distance(initial_state, goal_state)))
    #print(frontier.qsize())
    while not frontier.empty():
        node = frontier.get()
        #print(frontier.qsize())
        #print("Here1")

        if node.state == goal_state:
            return node, total_nodes

        if node.state not in visited:
            visited.append(node.state)
            #print("Here2")
            for action in ["E", "W", "N", "S", "U", "D"]:
                new_state = move(node.state, action)
                #print("Here3")
                if new_state is not None:
                    new_node = Node(new_state, node, action, node.cost + 1, manhattan_distance(new_state, goal_state))
                    frontier.put(new_node)
                    total_nodes += 1

    return None, total_nodes

    empty_z, empty_y, empty_x = find_position(state, 0)

    if action == "U" and empty_z > 0:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z - 1][empty_y][empty_x]
        new_state[empty_z - 1][empty_y][empty_x] = 0
        return new_state

    elif action == "D" and empty_z < 2:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z + 1][empty_y][empty_x]
        new_state[empty_z + 1][empty_y][empty_x] = 0
        return new_state
    
    elif action == "N" and empty_y > 0:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y - 1][empty_x]
        new_state[empty_z][empty_y - 1][empty_x] = 0
        return new_state

    elif action == "S" and empty_y < 2:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y + 1][empty_x]
        new_state[empty_z][empty_y + 1][empty_x] = 0
        return new_state
    
    elif action == "W" and empty_x > 0:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y][empty_x - 1]
        new_state[empty_z][empty_y][empty_x - 1] = 0
        return new_state

    elif action == "E" and empty_x < 2:
        new_state = copy.deepcopy(state)
        new_state[empty_z][empty_y][empty_x] = new_state[empty_z][empty_y][empty_x + 1]
        new_state[empty_z][empty_y][empty_x + 1] = 0
        return new_state
# Returns the nodes within the optimal path and total cost of each node, respectively.                
def output_optimal_path(node):
    optimal_path = []
    total_cost =[]
    while node is not None:
        optimal_path.insert(0, node.action)
        total_cost.insert(0, node.f())
        node = node.parent
    optimal_path.pop(0)                         # Since the action is "None", just removed it.
    return optimal_path, total_cost
# Read the initial and goal states.
def read_states(file):
    state = []
    goal = []
    with open(file, 'r') as file:
        for _ in range(3):
            layer = []
            for _ in range(3):
                row = file.readline().strip().split()
                for i in range(len(row)):
                    row[i] = int(row[i])
                layer.append(row)
            file.readline()
            state.append(layer)
        for _ in range(3, 6):
            layer = []
            for _ in range(3):
                # layer.append(file.readline().strip().split())
                row = file.readline().strip().split()
                for i in range(len(row)):
                    row[i] = int(row[i])
                layer.append(row)
            file.readline()
            goal.append(layer)
        return state, goal

initial_state = [
[[1, 2, 3], [4, 0, 5], [6, 7, 8]],  
[[9, 10, 11], [12, 13, 14], [15, 16, 17]],
[[18, 19, 20], [21, 22, 23], [24, 25, 26]]
]
goal_state = [
    [[1, 2, 3],[4, 5, 8],[6, 7, 17]],
    [[9, 10, 11], [12, 13, 14], [15, 25, 16]],
    [[18, 19, 20], [0, 21, 23], [24, 22, 26]]
]

initial_state, goal_state = read_states("input3.txt")

solution, total_nodes = a_star_search(initial_state, goal_state)
path, total_cost = output_optimal_path(solution)
depth = len(path)

print("Depth Level:", depth)
print("Nodes Generated:", total_nodes)
print("Optimal Path:", path)
print("f(n) of each node: ", total_cost)


# par = solution
# print(par.action)
# while par.parent != None:
#     par = par.parent
#     print(par.action)

# root_node = par
# print(root_node.state)
# print(root_node.action)


##########################################################################

# # def move(state, action):
#     """Moves the blank tile in the given direction."""

#     blank_x, blank_y, blank_z = find_position(state, 0)

#     if action == "E" and blank_x < 2:
#         new_state = copy.deepcopy(state)
#         new_state[blank_x][blank_y][blank_z] = new_state[blank_x + 1][blank_y][blank_z]
#         new_state[blank_x + 1][blank_y][blank_z] = 0
#         return new_state

#     elif action == "W" and blank_x > 0:
#         new_state = copy.deepcopy(state)
#         new_state[blank_x][blank_y][blank_z] = new_state[blank_x - 1][blank_y][blank_z]
#         new_state[blank_x - 1][blank_y][blank_z] = 0
#         return new_state

#     elif action == "N" and blank_y < 2:
#         new_state = copy.deepcopy(state)
#         new_state[blank_x][blank_y][blank_z] = new_state[blank_x][blank_y + 1][blank_z]
#         new_state[blank_x][blank_y + 1][blank_z] = 0
#         return new_state

#     elif action == "S" and blank_y > 0:
#         new_state = copy.deepcopy(state)
#         new_state[blank_x][blank_y][blank_z] = new_state[blank_x][blank_y - 1][blank_z]
#         new_state[blank_x][blank_y - 1][blank_z] = 0
#         return new_state

#     elif action == "U" and blank_z < 2:
#         new_state = copy.deepcopy(state)
#         new_state[blank_x][blank_y][blank_z] = new_state[blank_x][blank_y][blank_z + 1]
#         new_state[blank_x][blank_y][blank_z + 1] = 0
#         return new_state

#     elif action == "D" and blank_z > 0:
#         new_state = copy.deepcopy(state)
#         new_state[blank_x][blank_y][blank_z] = new_state[blank_x][blank_y][blank_z - 1]
#         new_state[blank_x][blank_y][blank_z - 1] = 0
#         return new_state
