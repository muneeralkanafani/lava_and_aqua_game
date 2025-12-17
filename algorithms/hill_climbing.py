import time
import element
from queue import PriorityQueue
from game_engine import GameEngine
from game_renderer.game_renderer import GameRenderer

class HillClimbing:
    def __init__(self, level_file, algorithm_name="Hill Climbing"):
        self.renderer = GameRenderer(cell_size=60)
        self.engine = GameEngine()
        self.level_file = level_file
        self.algorithm_name = algorithm_name
        self.states_explored = 0
        self.generated_states = 0

    def run(self):
        initial_state = element.LevelLoader.load_level(self.level_file)
        initial_node = Node(state=initial_state, cost=self.heuristic(initial_state))
        pq = PriorityQueue()
        pq.put(initial_node)
        best_cost = {initial_node.state: initial_node.cost}
        visited = set()
        start_time = time.time()
        goal_node = None

        while not pq.empty():
            current_node = pq.get()
            current_state = current_node.state
            if current_state in visited:
                continue
            visited.add(current_state)
            self.states_explored += 1
            if self.engine.goal_test(current_state):
                goal_node = current_node
                break
            moves = self.engine.all_valid_moves(current_state)
            if moves is None:
                continue
            for action in moves:
                new_state = self.engine.transition_model(current_state, action)
                if new_state is None:
                    continue
                heuristic = self.heuristic(new_state)
                new_cost = current_node.cost + heuristic
                if new_state not in best_cost or new_cost < best_cost[new_state]:
                    best_cost[new_state] = new_cost
                    new_node = Node(
                        state=new_state,
                        parent=current_node,
                        action=action,
                        cost=new_cost
                    )
                    pq.put(new_node)
                    self.generated_states += 1
            # self.render_each_step(current_state)

        end_time = time.time()
        elapsed_time = end_time - start_time

        if goal_node is not None:
            self.renderer.render_win_path(self.level_file,
                                          self.algorithm_name,
                                          self.states_explored,
                                          self.generated_states,
                                          goal_node.state,
                                          goal_node.state.path_cost,
                                          elapsed_time)

    def render_each_step(self, state):
        status_text = f"moves: {state.path_cost}"
        self.renderer.render(state, status_text)

    def heuristic(self, state):
        """
        the heuristic function (that should calculate for each node) is:
        the distance from the player to all goal_orbs to the goal
        eg: player -> goal_orb_1 -> goal_orb_2 -> goal
        """
        heuristic = 0
        if state.player_position is not None:
            player_position_dx, player_position_dy = state.player_position
            goal_position_dx, goal_position_dy = state.goal_position
            previous_goal_orb_dx, previous_goal_orb_dy = 0, 0
            for goal_orb_dx, goal_orb_dy in state.goal_orb_position:
                if previous_goal_orb_dx == 0 and previous_goal_orb_dy == 0:
                    heuristic += abs(goal_orb_dx - player_position_dx)
                    heuristic += abs(goal_orb_dy - player_position_dy)
                else:
                    heuristic += abs(goal_orb_dx - previous_goal_orb_dx)
                    heuristic += abs(goal_orb_dy - previous_goal_orb_dy)
                previous_goal_orb_dx = goal_orb_dx
                previous_goal_orb_dy = goal_orb_dy
            heuristic += abs(goal_position_dx - previous_goal_orb_dx)
            heuristic += abs(goal_position_dy - previous_goal_orb_dy)
        return heuristic

class Node:
    def __init__(self, state:element.GameState, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost
