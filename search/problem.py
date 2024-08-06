from abc import ABC, abstractmethod


class SearchProblem(ABC):

    @abstractmethod
    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        pass
    
    @abstractmethod
    def is_goal_state(self, state) -> bool:
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        pass

    @abstractmethod
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
        
        
    @abstractmethod
    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        pass
