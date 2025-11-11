import pygame

class ElementDrawer:
    def __init__(self):
        pass
        
    def draw_element(self, renderer, position, element):
        """Draw a single game element"""
        x, y = position
        screen_x = x * (renderer.cell_size + renderer.margin) + renderer.margin
        screen_y = y * (renderer.cell_size + renderer.margin) + renderer.margin
        cell_rect = pygame.Rect(
            screen_x, 
            screen_y, 
            renderer.cell_size, 
            renderer.cell_size
        )
        # Get color based on element type (background color)
        color = renderer.get_element_color(element.type)
        pygame.draw.rect(renderer.screen, color, cell_rect)
        # Add special rendering for different element types
        if element.type.name == 'NUMBERED_BLOCK':
            self.draw_numbered_block(renderer, cell_rect, element)
        elif element.type.name == 'AQUA':
            self.draw_aqua(renderer, cell_rect)
        elif element.type.name == 'WALL':
            self.draw_wall(renderer, cell_rect)
        elif element.type.name == 'MOVABLE_BLOCK':
            self.draw_movable_block(renderer, cell_rect)
        if element.properties.get('lava_wall', False) == True:
            self.draw_lava_wall(renderer, cell_rect)
        elif element.properties.get('goal_orb', False) == True:
            self.draw_goal_orb(renderer, cell_rect)
        elif element.properties.get('goal', False) == True:
            self.draw_goal(renderer, cell_rect)
        if element.properties.get('player', False) == True:
            self.draw_player(renderer, cell_rect)

    
    def draw_numbered_block(self, renderer, cell_rect, element):
        """Draw a numbered block with its move count"""
        moves = element.properties.get('moves_remaining', '?')
        text = renderer.large_font.render(str(moves), True, (28,79,21))
        text_rect = text.get_rect(center=cell_rect.center)
        renderer.screen.blit(text, text_rect)
        pygame.draw.rect(renderer.screen, (28,79,21), cell_rect, 3)
    
    def draw_player(self,renderer, cell_rect):
        """Draw the player with a special indicator"""
        pygame.draw.circle(
            renderer.screen,
            (200, 170, 130),
            cell_rect.center,
            renderer.cell_size // 2,
        )
        pygame.draw.circle(
            renderer.screen,
            (100, 100, 100),
            cell_rect.center,
            renderer.cell_size // 2,
            3
        )
    
    def draw_aqua(self, renderer, cell_rect):
        """Draw aqua with water-like effect"""
        center_y = cell_rect.centery
        points = [
            (cell_rect.left, center_y),
            (cell_rect.left + renderer.cell_size // 3, center_y - 3),
            (cell_rect.left + 2 * renderer.cell_size // 3, center_y + 3),
            (cell_rect.right, center_y)
        ]
        pygame.draw.lines(renderer.screen, (42,42,213), False, points, 4)
    
    def draw_lava_wall(self, renderer, cell_rect):
        """Draw lava and aqua wall shape"""
        center = cell_rect.center
        size = renderer.cell_size // 6
        for dx, dy in [(1,-1), (-1,-1), (1,1), (-1,1)]:
            points = [
                (center[0] + dx * size, center[1] + dy * size),
                (center[0] + dx * size, center[1] + dy * 3 * size),
                (center[0] + dx * 3 * size, center[1] + dy * 3 * size),
                (center[0] + dx * 3 * size, center[1] + dy * size),
            ]
            pygame.draw.polygon(renderer.screen, (120, 191, 220), points)
            pygame.draw.polygon(renderer.screen, (0,0,0), points, 2)

    def draw_wall(self, renderer, cell_rect):
        """Draw wall borders"""
        pygame.draw.rect(renderer.screen, (0,0,0), cell_rect, 2)

    def draw_movable_block(self, renderer, cell_rect):
        """Draw movable block borders and the points in it"""
        center = cell_rect.center
        size = renderer.cell_size // 3
        radius = renderer.cell_size // 15
        for dx, dy in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
            pos = (center[0] + dx * size, center[1] + dy * size)
            pygame.draw.circle(
                renderer.screen,
                (49, 49, 49),
                pos,
                radius
            )
        pygame.draw.rect(renderer.screen, (14,14,14), cell_rect, 2)
    
    def draw_goal(self, renderer, cell_rect):
        """Draw the goal with a special pattern"""
        pygame.draw.rect(renderer.screen, (156,125,193), cell_rect, 30)
        center = cell_rect.center
        sizes = [renderer.cell_size // 3, renderer.cell_size // 4.5, renderer.cell_size // 9]
        colors = [(35,34,36), (156,125,193), (35,34,36)]
        for size, color in zip(sizes, colors):
            points = [
                (center[0] + size, center[1] - size),
                (center[0] + size, center[1] + size),
                (center[0] - size, center[1] + size),
                (center[0] - size, center[1] - size),
            ]
            pygame.draw.polygon(renderer.screen, color, points)
        pygame.draw.rect(renderer.screen, (35,34,36), cell_rect, 5)

    def draw_goal_orb(self,renderer, cell_rect):
        """Draw the goal orb with a special indicator"""
        pygame.draw.circle(
            renderer.screen,
            (156,125,193),
            cell_rect.center,
            renderer.cell_size // 3,
        )
