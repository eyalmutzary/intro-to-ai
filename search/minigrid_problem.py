from problem import SearchProblem
from state import Action, GameState


class MinigridProblem(SearchProblem):
    def __init__(self, initial_state: GameState):
        self.state = initial_state
        # self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        # self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.state
        

    def is_goal_state(self, state: GameState):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return state.player_location == state.goal_location
            


    def get_successors(self, state: GameState):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        legal_actions = state.get_legal_actions()
        successors = []
        for action in legal_actions:
            successor = state.generate_successor(action)
            successors.append((successor, action, 1))
        return successors
    

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        # count left and right as 2 moves
        cost = 0
        for action in actions:
            if action in [Action.TURN_LEFT, Action.TURN_RIGHT]:
                cost += 2
            else:
                cost += 1
        return cost
