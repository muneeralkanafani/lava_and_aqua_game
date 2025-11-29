from enum import Enum
import csv

class ElementType(Enum):
    LAVA = 'L'
    AQUA = 'A'
    WALL = '#'
    MOVABLE_BLOCK = 'B'
    NUMBERED_BLOCK = 'N'
    GOAL = 'G'
    EMPTY = ' '

class GameElement:
    def __init__(self, element_type, position, properties = None):
        self.type = element_type
        self.position = position
        self.properties = properties or {
            'lava_wall': False,
            'goal_orb': False,
            'player': False,
            'goal': False
        }
    
class GameState:
    def __init__(self, elements, width: int, height: int,  parent=None, action=None, path_cost=0):
        self.elements = elements
        self.width = width
        self.height = height
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self._hash = None
        self.player_position = None
        self.goal_position = None
        self.lava_positions = set()
        self.aqua_positions = set()
        self.numbered_block_positions = set()
        self.goal_orb_position = set()

        for position, element in self.elements.items():
            props = element.properties
            if props.get("player", False):
                self.player_position = position
            if props.get("goal_orb", False):
                self.goal_orb_position.add(position)
            if props.get("goal", False):
                self.goal_position = position
            if element.type == ElementType.LAVA:
                self.lava_positions.add(position)
            elif element.type == ElementType.AQUA:
                self.aqua_positions.add(position)
            elif element.type == ElementType.NUMBERED_BLOCK:
                self.numbered_block_positions.add(position)
    
    def __hash__(self):
        if self._hash is None:
            # hash only element types & important properties
            items = tuple(sorted(
                (pos, e.type, tuple(sorted(e.properties.items())))
                for pos, e in self.elements.items()
            ))
            self._hash = hash(items)
        return self._hash

    def __eq__(self, other):
        return hash(self) == hash(other)

class LevelLoader:
    def load_level(filename: str) -> GameState:
        """
        take the level as a csv file and return a Game State
        """
        try:
            # Load level from csv file
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = [row for row in reader]
            if not lines:
                raise ValueError(f"Empty level file: {filename}")
            height = len(lines)
            width = len(lines[0]) if height > 0 else 0
            # Create a hash table (dictionary) for elements
            elements = {}
            for y, row in enumerate(lines):
                # give an error if any row didn't equal the width 
                if len(row) != width:
                    raise ValueError(f"Inconsistent row length in {filename} at row {y+1}")
                for x, cell in enumerate(row):
                    position = (x, y)
                    cell = cell.strip()
                    if not cell or cell == ' ':
                        continue
                    if cell == 'P':
                        elements[position] = GameElement(
                            ElementType.EMPTY,
                            position,
                            {'player': True}
                        )
                    elif cell == 'L':
                        elements[position] = GameElement(ElementType.LAVA, position)
                    elif cell == 'A':
                        elements[position] = GameElement(ElementType.AQUA, position)
                    elif cell == '#':
                        elements[position] = GameElement(ElementType.WALL, position)
                    elif cell == 'B':
                        elements[position] = GameElement(ElementType.MOVABLE_BLOCK, position)
                    elif cell == 'G':
                        elements[position] = GameElement(
                            ElementType.EMPTY,
                            position,
                            {'goal': True}
                        )
                    elif cell == 'O':
                        elements[position] = GameElement(
                            ElementType.EMPTY,
                            position,
                            {'goal_orb': True}
                        )
                    elif cell == 'W':
                        elements[position] = GameElement(
                            ElementType.EMPTY, 
                            position, 
                            {'lava_wall': True}
                        )
                    else:
                        # Check if it's a numbered block (numeric value)
                        try:
                            moves = int(cell)
                            elements[position] = GameElement(
                                ElementType.NUMBERED_BLOCK, 
                                position, 
                                {'moves_remaining': moves}
                            )
                        except ValueError:
                            # If not a number, treat as empty
                            continue
            return GameState(elements, width, height)
        except FileNotFoundError:
            raise FileNotFoundError(f"Level file not found: {filename}")
        except Exception as e:
            raise Exception(f"Error loading level {filename}: {str(e)}")
