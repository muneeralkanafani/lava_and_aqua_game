from element import GameElement, ElementType, GameState

class Direction:
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

class GameEngine:
    def __init__(self):
        self.directions = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0)
        }
    
    def transition_model(self, state, action):
        """
        Apply an action to the current state and return a new state
        Returns None if the move is invalid OR if player dies
        """
        # End the game (return None) if the action is not in directions
        if action not in self.directions:
            return None
        # Calculate direction
        dx, dy = self.directions[action]
        # End the game (return None) if there is no player
        player_position = state.player_position
        if player_position is None:
            return None
        # Calculate player new position
        new_position = (player_position[0] + dx, player_position[1] + dy)
        # Check if the move is valid (return None if not)
        if not self.is_valid_move(state, new_position, (dx, dy)):
            return None
        # Copy the element (new_elements)
        new_elements = self.fast_copy_elements(state.elements)
        # Move the player to the new position
        new_elements[player_position].properties['player'] = False
        if new_position in new_elements:
            new_elements[new_position].properties['player'] = True
        else:
            new_elements[new_position] = GameElement(ElementType.EMPTY, new_position, {'player': True})
        # Remove the GOAL ORB if the player on it
        if new_elements[new_position].properties.get('goal_orb', False):
            new_elements[new_position].properties['goal_orb'] = False
        # Handle block pushing if necessary
        self.push_block(new_elements, new_position, (dx, dy))        
        # Update blocks (numbered - lava - aqua)
        self.update_numbered_blocks(new_elements, state.numbered_blocks)
        self.update_lava_blocks(new_elements, state.lava_positions)
        self.update_aqua_blocks(new_elements, state.aqua_positions)
        # Return new state
        return GameState(
            elements=new_elements,
            width=state.width,
            height=state.height,
            parent=state,
            action=action,
            path_cost=state.path_cost + 1
        )
    
    def all_valid_moves(self, state):
        """
        check all the four moves up, down, left and right
        which can be valid
        """
        if state.player_position is None:
            return []
        all_valid_move = []
        for direction in self.directions:
            dx, dy = self.directions[direction]
            new_position = (state.player_position[0] + dx, state.player_position[1] + dy)
            can_move = self.is_valid_move(state, new_position, (dx, dy))
            if can_move:
                all_valid_move.append(direction)
            else:
                continue
        return all_valid_move

    def is_valid_move(self, state, new_position, direction):
        """
        Check if moving to new position is valid
        return True if the new position is valid and false if it doesn't
        """
        x, y = new_position
        # Check if the new player position is outside the map 
        if x < 0 or x >= state.width or y < 0 or y >= state.height:
            return False
        # Check if the player can move to the target block
        target_element = state.elements.get(new_position)
        if target_element is None:
            return True
        if (target_element.type in [ElementType.WALL, ElementType.NUMBERED_BLOCK]
              or target_element.properties.get('lava_wall', False)
              ):
            return False
        elif target_element.type == ElementType.MOVABLE_BLOCK:
            return self.can_push_block(state, new_position, direction)
        return True
    
    def can_push_block(self, state, block_position, direction):
        """
        Check if a block can be pushed in the given direction
        return True if it can and False if it can't
        """
        dx, dy = direction
        new_block_position = (block_position[0] + dx, block_position[1] + dy)
        x, y = new_block_position
        # Check if the new block position outside the map 
        if x < 0 or x >= state.width or y < 0 or y >= state.height:
            return False
        # Check if the space beyond the block is free
        target_element = state.elements.get(new_block_position)
        if target_element is None:
            return True
        elif (target_element.type in [
            ElementType.WALL,
            ElementType.MOVABLE_BLOCK,
            ElementType.NUMBERED_BLOCK] 
            or target_element.properties.get('goal', False)
            or target_element.properties.get('lava_wall', False)
            ):
            return False
        return True
    
    def push_block(self, elements, new_position, direction):
        """
        Push the block to the new position 
        and leave the GOAL ORB behind if it is on the old block position
        and don't remove it if it is on the new block position
        """
        dx, dy = direction
        target_element = elements.get(new_position)
        if target_element and target_element.type == ElementType.MOVABLE_BLOCK:
            # Calculate the block new position
            block_new_position = (new_position[0] + dx, new_position[1] + dy)
            # Empty the old block position
            elements[new_position].type = ElementType.EMPTY
            # Check if there is a GOAL ORB at the old block position
            # if the old block position has GOAL ORB (leave the GOAL ORB behind)
            if elements[new_position].properties.get('goal_orb', False):
                elements[new_position].properties['goal_orb'] = True
            # Move the block and don't remove GOAL_ORB from new block position
            new_block = GameElement(ElementType.MOVABLE_BLOCK, block_new_position)
            if block_new_position not in elements:
                elements[block_new_position] = new_block
            else:
                elements[block_new_position].type = ElementType.MOVABLE_BLOCK
    
    def update_numbered_blocks(self, elements, numbered_position):
        """Decrement moves on numbered blocks and remove if zero"""
        blocks_to_remove = []
        for position in numbered_position:
            block = elements.get(position)
            if block:
                block.properties['moves_remaining'] -= 1
                if block.properties['moves_remaining'] <= 0:
                    blocks_to_remove.append(position)
        # Remove the blocks when the numbered block hits zero
        for position in blocks_to_remove:
            del elements[position]

    def update_lava_blocks(self, elements, lava_positions):
        """Make the lave blocks spread up, down, left and right"""
        # Find the new lava blocks 
        new_lava_to_add = set()
        positions_to_remove = set()
        for lava_position in lava_positions:
            if elements.get(lava_position).type == ElementType.MOVABLE_BLOCK:
                continue
            # Check for each direction to the LAVA block if it can spread
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_position = (lava_position[0] + dx, lava_position[1] + dy)
                target_element = elements.get(new_position)
                if target_element is None:
                    new_lava_to_add.add(new_position)
                elif (target_element.type == ElementType.LAVA 
                    and target_element.properties.get('player', False)):
                    new_lava_to_add.add(new_position)
                elif target_element.type in [
                    ElementType.WALL,
                    ElementType.MOVABLE_BLOCK,
                    ElementType.NUMBERED_BLOCK,
                    ElementType.LAVA
                ]:
                    continue
                elif (target_element.properties.get('lava_wall', False)
                     or target_element.properties.get('goal_orb', False)
                     or target_element.properties.get('goal', False)
                     ):
                    positions_to_remove.add(new_position)
                elif (target_element.properties.get('player', False)
                      or target_element.type == ElementType.EMPTY
                      ):
                    new_lava_to_add.add(new_position)
        for position in positions_to_remove:
            if position in elements:
                elements[position].type = ElementType.LAVA
        for position in new_lava_to_add:
            elements[position] = GameElement(ElementType.LAVA, position)
    
    def update_aqua_blocks(self, elements, aqua_positions):
        """Make the aqua blocks spread up, down, left and right"""
        # Find the new aqua blocks
        new_aqua_to_add = set()
        positions_to_steam = set()
        positions_to_remove = set()
        for aqua_position in aqua_positions:
            if elements.get(aqua_position).type == ElementType.MOVABLE_BLOCK:
                continue
            # Check for each direction to the AQUA block if it can spread
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_position = (aqua_position[0] + dx, aqua_position[1] + dy)
                target_element = elements.get(new_position)
                if target_element is None:
                    new_aqua_to_add.add(new_position)
                elif target_element.type in [
                    ElementType.WALL,
                    ElementType.MOVABLE_BLOCK,
                    ElementType.NUMBERED_BLOCK,
                    ElementType.AQUA
                ]:
                    continue
                elif (target_element.properties.get('lava_wall', False)
                      or target_element.properties.get('goal_orb', False)
                      or target_element.properties.get('player', False) 
                      or target_element.properties.get('goal', False)
                      ):
                    positions_to_remove.add(new_position)
                elif target_element.type == ElementType.EMPTY:
                    new_aqua_to_add.add(new_position)
                elif target_element.type == ElementType.LAVA:
                    positions_to_steam.add(new_position)
        for position in positions_to_remove:
            if position in elements:
                elements[position].type = ElementType.AQUA
        for position in positions_to_steam:
            elements[position] = GameElement(ElementType.WALL, position)
        for position in new_aqua_to_add:
            elements[position] = GameElement(ElementType.AQUA, position)
    
    def is_player_dead(self, state):
        """Check if player was killed by lava (no player found in elements)"""
        if state.player_position == None:
            return True
        return False
    
    def goal_test(self, state):
        """Check if the player reached the goal - returns True if yes"""
        return state.player_position == state.goal_position and len(state.goal_orb_position) == 0
        
    def fast_copy_elements(self, elements):
        return {
            pos: GameElement(e.type, e.position, e.properties.copy())
            for pos, e in elements.items()
        }

