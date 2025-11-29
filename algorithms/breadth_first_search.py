import pygame
import element
import time
from collections import deque
from game_engine import GameEngine
from game_renderer.game_renderer import GameRenderer

class BreadthFirstSearch:
    def __init__(self, level_file,algorithm_name="BFS"):
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
        visited.add(hash(self.initial_state))
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
            for direction in all_valid_move:
                add_state = self.engine.transition_model(current_state, direction)
                if add_state is None:
                    continue
                h = hash(add_state)
                if h not in visited:
                    visited.add(h)
                    status.append(add_state)
                    self.generated_states += 1
            # self.render_each_step(current_state)
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        if player_win:
            self.render_win_path(current_state, current_state.path_cost, elapsed_time)

    def render_win_path(self, goal_state, path_cost, elapsed_time):
        actions = []
        states = []
        current = goal_state
        clock = pygame.time.Clock()

        while current.parent is not None:
            actions.append(current.action)
            states.append(current)
            current = current.parent

        states.append(current)

        actions.reverse()
        states.reverse()

        for current_state in states:
            status_text = f"moves: {current_state.path_cost}"
            self.renderer.render(current_state, status_text)
            time.sleep(0.2)

        keep_window_open = True
        while keep_window_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_window_open = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keep_window_open = False
            status_text = f"moves: {current_state.path_cost}"
            message = f"path cost {current_state.path_cost} - time {elapsed_time} - states explored {self.states_explored}"
            self.renderer.render_with_message(current_state, status_text, message)
            clock.tick(60)
        pygame.quit()

        print("-"*100)
        print(f"the level: {self.level_file}")
        print(f"the algorithm: {self.algorithm_name}")
        print(f"path cost: {path_cost}")
        print(f"time: {elapsed_time}")
        print(f"state explored: {self.states_explored}")
        print(f"state generated: {self.generated_states}")
        print("-"*100)

    def render_each_step(self, state):
        status_text = f"moves: {state.path_cost}"
        self.renderer.render(state, status_text)
