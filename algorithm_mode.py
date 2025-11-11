from game_renderer.game_renderer import GameRenderer
from game_engine import GameEngine

class AlgorithmMode:
    def __init__(self, level_file, algorithm, duration):
        self.renderer = GameRenderer(cell_size=60)
        self.engine = GameEngine()
        self.level_file = level_file
        self.algorithm = algorithm
        self.duration = duration
    
    def run(self):
        print(f"the level: {self.level_file}")
        print(f"the algorithm: {self.algorithm}")
        print(f"the duration: {self.duration}")
