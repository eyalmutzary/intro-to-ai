from agents import Agent
from game_state import GameState

class AlphaBetaAgent(Agent):
    
    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        MAX_AGENT = 0
        MIN_AGENT = 1
        
        def alpha_beta(state: GameState, depth, alpha, beta, agent: int):
            if depth == 0 or len(state.get_legal_actions()) == 0:
                return self.evaluation_function(state)
            
            if agent == MAX_AGENT:
                best_value = float('-inf')
                best_action = None
                for action in state.get_legal_actions():
                    successor = state.generate_successor(action)
                    curr_value = alpha_beta(successor, depth - 1, alpha, beta, MIN_AGENT)
                    if curr_value > best_value:
                        best_value = curr_value
                        best_action = action
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break  # cutoff
                if depth == self.depth:
                    return best_action  # root node action
                else:
                    return best_value
            else:  # Min player
                best_value = float('inf')
                for action in state.get_legal_actions():
                    successor = state.generate_successor(action)
                    curr_value = alpha_beta(successor, depth, alpha, beta, MAX_AGENT)
                    best_value = min(best_value, curr_value)
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break  # cutoff
                return best_value
            
        return alpha_beta(game_state, self.depth, float('-inf'), float('inf'), MAX_AGENT).value


    # def get_state_representation(self, game_state):
    #     # Convert game_state to our state representation
    #     pass

    # def is_goal_state(self, state):
    #     # Check if the state is a goal state
    #     pass

    # def get_legal_actions(self, state):
    #     # Return legal actions for the given state
    #     pass

    # def get_next_state(self, state, action):
    #     # Apply action to state and return the resulting state
    #     pass

    # def heuristic(self, state):
    #     # Implement heuristic function (e.g., Manhattan distance to goal)
    #     pass