from algorithms.breadth_first_search import BreadthFirstSearch
from algorithms.depth_first_search import DepthFirstSearch
from algorithms.hill_climbing import HillClimbing
from algorithms.uniform_cost_search import UniformCostSearch
from game_renderer.game_renderer import GameRenderer
from game_engine import GameEngine

class AlgorithmMode:
    def __init__(self, level_file, algorithm):
        self.renderer = GameRenderer(cell_size=60)
        self.engine = GameEngine()
        self.level_file = level_file
        self.algorithm = algorithm
    
    def run(self):
        the_algorithm = self.algorithm.lower()
        if the_algorithm in ["dfs", "depth first search"]:
            dfs = DepthFirstSearch(self.level_file)
            dfs.run()
        elif the_algorithm in ["bfs", "breadth first search"]:
            bfs = BreadthFirstSearch(self.level_file)
            bfs.run()
        elif the_algorithm in ["ucs", "uniform cost search"]:
            ucs = UniformCostSearch(self.level_file)
            ucs.run()
        elif the_algorithm in ["hc", "hill climbing"]:
            hc = HillClimbing(self.level_file)
            hc.run()
