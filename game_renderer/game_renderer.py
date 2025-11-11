import pygame
from .element_drawer import ElementDrawer

class GameRenderer:
    def __init__(self, cell_size=60, margin=2):
        # Initialize pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
        self.cell_size = cell_size
        self.margin = margin
        self.screen = None
        self.font = None
        # Define colors for each element type (background color for each)
        self.colors = {
            'LAVA': (255,60,0),
            'AQUA': (28,28,162),
            'WALL': (120, 191, 220),
            'MOVABLE_BLOCK': (179,179,179),
            'NUMBERED_BLOCK': (132,220,120),
            'GOAL': (156,125,193),
            'EMPTY': (230,230,230),
            'BACKGROUND': (230,230,230),
            'GRID': (60, 60, 60)
        }
        # Load fonts
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.element_drawer = ElementDrawer()

    def render(self, game_state, additional_text=None):
        """Main render function - draws the entire game state"""
        if self.screen is None:
            self.initialize_screen(game_state)
        # Draw the grid background
        self.draw_grid(game_state)
        # Draw all game elements
        for position, element in game_state.elements.items():
            self.draw_element(position, element)
        # Draw additional text if provided
        if additional_text:
            self.draw_text(additional_text)
        # Update the display
        pygame.display.flip()
    
    def initialize_screen(self, game_state):
        """Create the pygame screen based on game state dimensions"""
        screen_width = game_state.width * (self.cell_size + self.margin) + self.margin
        screen_height = game_state.height * (self.cell_size + self.margin) + self.margin
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("LAVA AND AQUA GAME")
        return self.screen
    
    def draw_grid(self, game_state):
        """Draw the background grid"""
        self.screen.fill(self.colors['BACKGROUND'])
        # Draw grid lines
        for x in range(game_state.width + 1):
            line_x = x * (self.cell_size + self.margin)
            pygame.draw.line(
                self.screen, 
                self.colors['GRID'],
                (line_x, 0),
                (line_x, self.screen.get_height()),
                1
            )
        for y in range(game_state.height + 1):
            line_y = y * (self.cell_size + self.margin)
            pygame.draw.line(
                self.screen,
                self.colors['GRID'],
                (0, line_y),
                (self.screen.get_width(), line_y),
                1
            )

    def draw_element(self, position, element):
        """Draw a single game element"""
        self.element_drawer.draw_element(self, position, element)
    
    def draw_text(self, text):
        """Draw text at the top of the screen"""
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 20))
        self.screen.blit(text_surface, text_rect)

    def render_with_message(self, game_state, status_text, message=None):
        """Render the game state with message (optional) when game over or victory"""
        # Regular rendering
        self.render(game_state, status_text)
        # Draw centered message if provided
        if message:
            self.draw_centered_message(message)
        # Update display
        pygame.display.flip()

    def draw_centered_message(self, message, background_color=(0, 0, 0, 180), text_color=(255, 255, 255)):
        """Draw a centered message box with transparent background"""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill(background_color)
        self.screen.blit(overlay, (0, 0))
        # Create message text
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, text_color)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        # Create a background box for the text
        box_padding = 20
        box_rect = pygame.Rect(
            text_rect.left - box_padding,
            text_rect.top - box_padding,
            text_rect.width + 2 * box_padding,
            text_rect.height + 2 * box_padding
        )
        # Draw the box
        pygame.draw.rect(self.screen, (50, 50, 50), box_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), box_rect, width=2, border_radius=10)
        # Draw the text
        self.screen.blit(text, text_rect)
        # Add instruction text
        instruction_font = pygame.font.Font(None, 24)
        instruction_text = instruction_font.render("Press R to restart or ESC to quit or U to undo", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(self.screen.get_width() // 2, text_rect.bottom + 40))
        self.screen.blit(instruction_text, instruction_rect)

    def get_element_color(self, element_type):
        """Get the color for a specific element type"""
        return self.colors.get(element_type.name, self.colors['EMPTY'])
    
    def close(self):
        """Close the pygame window"""
        pygame.quit()
