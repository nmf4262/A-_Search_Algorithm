import queue
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


    #             if state[i][j][k] != goal_state[i][j][k]:
    #                 distance += abs(i - goal_state[i][j][k]) + abs(j - goal_state[j][k][k]) + abs(k - goal_state[k][j][k])
    # return distance

def a_star_search(initial_state, goal_state):
    """Performs the A* search algorithm to find a solution to the 26-puzzle problem."""

    frontier = queue.PriorityQueue()
    visited = []

    frontier.put(Node(initial_state, None, None, 0, manhattan_distance(initial_state, goal_state)))

    while not frontier.empty():
        node = frontier.get()
        # print(node.action)

        if node.state == goal_state:
            print("Hello")
            return node

        if node.state not in visited:
            visited.append(node.state)

            for action in ["E", "W", "N", "S", "U", "D"]:
                new_state = move(node.state, action)

                if new_state is not None:
                    new_node = Node(new_state, node, action, node.cost + 1, manhattan_distance(new_state, goal_state))
                    frontier.put(new_node)
            print(frontier.get().action)
    return None

def move(state, action):
    """Moves the blank tile in the given direction."""

    blank_x, blank_y, blank_z = find_position(state, 0)

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
                
def reconstruct_path(node):
    """Reconstructs the path from the goal node to the initial node."""
    path = []
    while node is not None:
        path.insert(0, node.action)
        node = node.parent
    return path


initial_state = [
[[1, 2, 3], [4, 0, 5], [6, 7, 8]],  
[[9, 10, 11], [12, 13, 14], [15, 16, 17]],
[[18, 19, 20], [21, 22, 23], [24, 25, 26]]
]

goal_state = [
    [[1, 2, 3],[4, 13, 5],[6, 7, 8]],
    [[9, 10, 11], [15, 12, 14], [24, 16, 17]],
    [[18, 19, 20], [21, 0, 23], [25, 22, 26]]
]


solution = a_star_search(initial_state, goal_state)
print(solution)
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
