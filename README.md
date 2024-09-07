Welcome to our Minigrid AI agents project.
Contributers:
    Eyal Mutzary 206910432
    Lior Gefen 315635136
    Yotam Cohen 319072864
The project is based on the Minigrid environment, which is a simple grid world environment for training agents.
developed by gymnasium.
The project includes 2 different agents:
1. Q-learning agent
2. Search agent

**Prerequisites**
Before running the project, ensure you have the following dependencies installed:

Python Version: Python 3.7 or higher

Libraries and Modules:

gymnasium (formerly known as OpenAI Gym)
minigrid (Gym-MiniGrid environment)
numpy (for numerical computations)
pandas (for data manipulation and CSV handling)
enum (for working with enumerations)
csv (for handling CSV files)
time (for handling timing operations)
collections (for data structures like defaultdict, deque)
copy (for copying objects)
typing (for type annotations and hints)
Custom Modules and Files:

constants (your custom constants file)
maps (your custom maps file)
problem (for handling search problems)
state (for handling game states)
search_algorithms (contains search algorithms like A* and improved heuristics)
util (utility functions, if any **FROM EX6**)
RL_Agents (for reinforcement learning agents like Q-learning)
CustomMinigridWrapper (your custom wrapper for MiniGrid)
Gym-MiniGrid Wrappers:

RGBImgPartialObsWrapper
ImgObsWrapper
ViewSizeWrapper
SymbolicObsWrapper
ActionBonus
PositionBonus
Installation
You can install the required libraries via pip:

bash
Copy code
pip install gymnasium minigrid numpy pandas
For the custom modules and files (constants.py, maps.py, problem.py, state.py, search_algorithms.py, util.py, etc.),
ensure they are in the correct directory or package structure within your project.

Acknowledgments
    MiniGrid
    Gymnasium