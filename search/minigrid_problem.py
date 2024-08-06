from problem import SearchProblem
from collections import deque

class MinigridProblem(SearchProblem):
    def __init__(self):
        pass
        # self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        # self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        pass
        # return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        pass
        # return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        pass
        # Note that for the search problem, there is only one player - #0
        # self.expanded = self.expanded + 1
        # return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)
