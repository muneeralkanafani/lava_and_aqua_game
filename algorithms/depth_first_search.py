import element
import time
from game_engine import GameEngine
from game_renderer.game_renderer import GameRenderer

class DepthFirstSearch:
    def __init__(self, level_file, algorithm_name="DFS"):
        self.renderer = GameRenderer(cell_size=60)
        self.engine = GameEngine()
        self.level_file = level_file
        self.algorithm_name = algorithm_name
        self.states_explored = 0
        self.generated_states = 0

    def run(self):
        self.initial_state = element.LevelLoader.load_level(self.level_file)
        start_time = time.time()
        status = [self.initial_state]
        visited = set()
        visited.add(self.initial_state)
        self.generated_states += 1
        player_win = False

        while status:
            current_state = status.pop()
            self.states_explored += 1
            if self.engine.goal_test(current_state):
                player_win = True
                break
            all_valid_move = self.engine.all_valid_moves(current_state)
            if all_valid_move is None:
                continue
            for direction in all_valid_move:
                add_state = self.engine.transition_model(current_state, direction)
                if add_state is None:
                    continue
                if add_state not in visited:
                    visited.add(add_state)
                    status.append(add_state)
                    self.generated_states += 1
            # self.render_each_step(current_state)

        end_time = time.time()
        elapsed_time = end_time - start_time

        if player_win:
            self.renderer.render_win_path(self.level_file,
                                          self.algorithm_name,
                                          self.states_explored,
                                          self.generated_states,
                                          current_state,
                                          current_state.path_cost,
                                          elapsed_time)

    def render_each_step(self, state):
        status_text = f"moves: {state.path_cost}"
        self.renderer.render(state, status_text)
    