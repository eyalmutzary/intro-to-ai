# import heapq
# from game_state import GameState, Action
# from agents import Agent
# import random
# import json

# class PlanningAgent(Agent):
    
#     def get_action(self, game_state: GameState):
#         path = self.a_star_search(game_state)
#         print(path)
#         if not path:
#             # If no path is found, return a random legal action
#             return random.choice(game_state.get_legal_actions()).value
#         return path[0].value

#     def a_star_search(self, start_state: GameState):
#         frontier = [(0, start_state, [])]
#         explored = set()

#         while frontier:
#             current_cost, current_state, path = heapq.heappop(frontier)

#             if self.is_goal_state(current_state):
#                 return path

#             state_hash = self.state_to_hash(current_state)
#             if state_hash in explored:
#                 continue

#             explored.add(state_hash)
#             print(path)
#             # if len(path) >= self.depth:
#             #     continue

#             for action in current_state.get_legal_actions():
#                 next_state = current_state.generate_successor(action)
#                 new_path = path + [action]
#                 priority = len(new_path) + self.heuristic(next_state)
#                 heapq.heappush(frontier, (priority, next_state, new_path))

#         return []

#     def is_goal_state(self, state: GameState):
#         player_location = state.player_location
#         return state.observation[player_location[0]][player_location[1]] == 'goal'

#     def heuristic(self, state: GameState):
#         return -self.evaluation_function(state)

#     def state_to_hash(self, state: GameState):
#         return (state.player_location, json.dumps(state.observation))



from game_state import GameState, Action
from agents import Agent
import random
import json

class PlanningAgent(Agent):
    
    def get_action(self, game_state: GameState):
        # def dfs(state: GameState, depth):
        #     if depth == 0 or not state.get_legal_actions():
        #         return self.evaluation_function(state), None

        #     best_value = float('-inf')
        #     best_action = None

        #     for action in state.get_legal_actions():
        #         successor = state.generate_successor(action)
        #         value, _ = dfs(successor, depth - 1)
        #         if value > best_value:
        #             best_value = value
        #             best_action = action

        #     return best_value, best_action

        # _, best_action = dfs(game_state, self.depth)
        # print(_, best_action)
        # return best_action.value
        # def depth_first_search(problem):
        
        
        fringe = []
        fringe.append((game_state), [])
        
        visited = set()

        while not len(fringe) == 0:
            state, actions = fringe.pop()
            state = self.hash_to_state(state)
            print(state)
            
            if self.is_goal_state(state):
                return actions

            if state not in visited:
                visited.add(self.state_to_hash(state))

                # for successor in game_state.generate_successor(state):
                for action in state.get_legal_actions():
                    successor = state.generate_successor(action)
                    if self.state_to_hash(successor) not in visited:
                        fringe.append((self.state_to_hash(successor), actions + [action.value]))

        return []
    
    def is_goal_state(self, state: GameState):
        player_location = state.player_location
        return state.observation[player_location[0]][player_location[1]] == 'goal'

    # def heuristic(self, state: GameState):
    #     return -self.evaluation_function(state)

    def state_to_hash(self, state: GameState):
        return (state.player_location, state._raw_observation)
    
    def hash_to_state(self, hash):
        player_location, observation = hash
        return GameState(observation, player_location)