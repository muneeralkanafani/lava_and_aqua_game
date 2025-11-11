import pygame
import element
from game_renderer.game_renderer import GameRenderer
from game_engine import GameEngine, Direction

class PlayerMode:
    def __init__(self, level_file):
        self.renderer = GameRenderer(cell_size=60)
        self.engine = GameEngine()
        self.level_file = level_file
        self.load_level()
        
    def load_level(self):
        print("Level loading .....")
        self.current_state = element.LevelLoader.load_level(self.level_file)
        self.initial_state = self.current_state
        print("Level loaded! Use arrow keys to move. Press ESC to quit.")
        print("Press U to undo, R to restart level")

    def run(self):
        # Initial render
        self.update_display()
        clock = pygame.time.Clock()
        running = True
        while running:
            running, moved = self.handle_events()
            if moved:
                self.update_display()
            clock.tick(8)
        self.renderer.close()

    def update_display(self):
        status_text = f"Moves: {self.current_state.path_cost}"
        message = None
        if self.engine.goal_test(self.current_state):
            status_text += " - YOU WIN!"
            message = "VICTORY!"
        elif self.engine.is_player_dead(self.current_state):
            status_text += " - GAME OVER! You died!"
            message = "GAME OVER"
        if message:
            self.renderer.render_with_message(self.current_state, status_text, message)
        else:
            self.renderer.render(self.current_state, status_text)
    
    def handle_events(self):
        moved = False
        keys = pygame.key.get_pressed()
        # Stop the game when the player QUIT the game (return running False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, moved
        # Stop the game when the player hits ESCAPE key (return running False)
        if keys[pygame.K_ESCAPE]:
            return False, moved
        # Undo one state when the player hits U key
        if keys[pygame.K_u]:
            if self.current_state.parent:
                self.current_state = self.current_state.parent
                moved = True
        # Restart the game when the player hits R key
        if keys[pygame.K_r]:
            self.current_state = self.initial_state
            moved = True
        # Handle up, down, left and right moving
        if not moved:
            direction = self.get_direction_from_keys(keys)
            if direction:
                new_state = self.engine.transition_model(self.current_state, direction)
                if new_state:
                    self.current_state = new_state
                    moved = True
        return True, moved
    
    def get_direction_from_keys(self, keys):
        if keys[pygame.K_UP]:
            return Direction.UP
        elif keys[pygame.K_DOWN]:
            return Direction.DOWN
        elif keys[pygame.K_LEFT]:
            return Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            return Direction.RIGHT
        return None
