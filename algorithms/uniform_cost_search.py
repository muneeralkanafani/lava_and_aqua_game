import time
import element
from queue import PriorityQueue
from game_engine import GameEngine
from game_renderer.game_renderer import GameRenderer

class UniformCostSearch:
    def __init__(self, level_file, algorithm_name="UCS"):
        self.renderer = GameRenderer(cell_size=60)
        self.engine = GameEngine()
        self.level_file = level_file
        self.algorithm_name = algorithm_name
        self.states_explored = 0
        self.generated_states = 0

    def run(self):
        initial_state = element.LevelLoader.load_level(self.level_file)
        initial_node = Node(initial_state)
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
                new_cost = self.path_cost(current_node, new_state)
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
    
    def path_cost(self, node, new_state):
        """
        the path cost function (that should calculate for each node) is:
        the number of new lava + the previous node cost
        """
        parent_lava = len(node.state.lava_positions)
        child_lava = len(new_state.lava_positions)
        delta_lava = max(0, child_lava - parent_lava)
        new_cost = node.cost + delta_lava
        return new_cost

class Node:
    def __init__(self, state:element.GameState, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost
