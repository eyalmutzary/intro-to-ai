import util
import time
from problem import SearchProblem

def depth_first_search(problem: SearchProblem):
    start = time.time()
    
    fringe = util.Stack()
    fringe.push((problem.get_start_state(), []))
    visited = set()

    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if problem.is_goal_state(state):
            print(f"#DFS# Time: {time.time() - start} , Expanded: {len(visited)}, Result: {len(actions)}")
            return actions

        if str(state) not in visited:
            visited.add(str(state))
            for successor, action, step_cost in problem.get_successors(state):
                if str(successor) not in visited:
                    fringe.push((successor, actions + [action]))

    return []


def breadth_first_search(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    start = time.time()
    fringe = util.Queue()
    fringe.push((problem.get_start_state(), []))
    visited = set()

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.is_goal_state(state):
            print(f"#BFS# Time: {time.time() - start} , Expanded: {len(visited)}, Result: {len(actions)}")
            return actions

        if state not in visited:
            visited.add(state)

            for successor, action, step_cost in problem.get_successors(state):
                if successor not in visited:
                    fringe.push((successor, actions + [action]))

    return []

class Node:
    """
        Represents a node in the graph
    """
    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

def uniform_cost_search(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    start = time.time()
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.get_start_state(), []), 0) # using node to be comparable

    visited = set()

    while not fringe.isEmpty():
        current_node = fringe.pop()
        state, actions = current_node.state, current_node.actions

        if problem.is_goal_state(state):
            print(f"#UCS# Time: {time.time() - start} , Expanded: {len(visited)}, Result: {len(actions)}")
            return actions

        if state not in visited:
            visited.add(state)

            for successor, action, step_cost in problem.get_successors(state):
                if successor not in visited:
                    new_actions = actions + [action]
                    next_possible_node = Node(successor, new_actions)
                    priority = problem.get_cost_of_actions(new_actions)
                    fringe.push(next_possible_node, priority)

    return []


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def improved_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return abs(state.player_location[0] - state.goal_location[0]) + abs(state.player_location[1] - state.goal_location[1])


def a_star_search(problem: SearchProblem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    start = time.time()

    fringe = util.PriorityQueue()
    initial_state = problem.get_start_state()
    fringe.push(Node(initial_state, []), 0 + heuristic(initial_state, problem))
    visited = set()

    while not fringe.isEmpty():
        current_node: Node = fringe.pop()
        state, actions = current_node.state, current_node.actions


        if problem.is_goal_state(state):
            print(f"#A*# Time: {time.time() - start} , Expanded: {len(visited)}, Result: {len(actions)}")
            return actions

        if state not in visited:
            visited.add(state)

            for successor, action, step_cost in problem.get_successors(state):
                if successor not in visited:
                    new_actions = actions + [action]
                    priority = problem.get_cost_of_actions(new_actions) + heuristic(successor, problem)
                    fringe.push(Node(successor, new_actions), priority)

    return []
