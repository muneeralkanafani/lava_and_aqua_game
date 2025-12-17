import element
import time
from collections import deque
from game_engine import GameEngine
from game_renderer.game_renderer import GameRenderer

class BreadthFirstSearch:
    def __init__(self, level_file, algorithm_name="BFS"):
        self.renderer = GameRenderer(cell_size=60)
        self.engine = GameEngine()
        self.level_file = level_file
        self.algorithm_name = algorithm_name
        self.states_explored = 0
        self.generated_states = 0

    def run(self):
        self.initial_state = element.LevelLoader.load_level(self.level_file)
        start_time = time.time()
        status = deque([self.initial_state])
        visited = set()
        visited.add(self.initial_state)
        self.generated_states += 1
        player_win = False

        while status:
            current_state = status.popleft()
            self.states_explored += 1
            if self.engine.goal_test(current_state):
                player_win = True
                break
            all_valid_move = self.engine.all_valid_moves(current_state)
            if all_valid_move is None:
                continue
            for action in all_valid_move:
                new_state = self.engine.transition_model(current_state, action)
                if new_state is None:
                    continue
                if new_state not in visited:
                    visited.add(new_state)
                    status.append(new_state)
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
