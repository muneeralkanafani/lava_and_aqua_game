# Lava and Aqua — a simple Python + Pygame puzzle

> Guide the player to the goal after collecting all goal orbs. Move safely on **aqua** and avoid touching **lava** — one hit and you're dead.

---

## About

**Lava and Aqua** is a small 2D puzzle / grid game written in **Python** using **Pygame**. The objective is simple: collect all the goal-orbs on a level, then reach the goal tile. The player can safely walk on aqua tiles; lava tiles kill the player; movable_blocks can block lava and aqua; lava_walls block player movement, but lava and aqua can move through them; numbered_blocks disappear after a fixed number of moves. This repository contains the game logic, level files and an algorithm mode for automated solving/testing.

## Features

* Play levels locally using the player mode.
* Algorithm mode to run pathfinding/AI logic over levels (see the `algorithms/` folder).
* Multiple levels stored under the `levels/` folder.
* Simple, easy-to-read Python + Pygame code (great for learning or extending).

## Requirements

* Python 3.8+ (should also work on newer 3.x versions)
* Pygame

Install the main dependency with pip:

```bash
pip install pygame
```

> If you use a virtual environment (recommended):
>
> ```bash
> python -m venv venv
> source venv/bin/activate   # Linux / macOS
> venv\Scripts\activate    # Windows
> pip install pygame
> ```

## Run the game

From the project root run:

```bash
python ./main.py <level_file> <algorithm_name>
```

* `<level_file>` — CSV level file located in the `levels/` folder.
* `<algorithm_name>` — (optional) name of the algorithm to run.

Example:

```bash
python ./main.py level1.csv a_star
```

## Controls

The game uses keyboard input for player movement. If you want to confirm or change the exact keys, open `player_mode.py` and look for the key handling section. Typically arrow keys are used for movement.

## Levels

Level data is stored in the `levels/` folder. You can add new level files following the format used by the existing levels — open one of the files in `levels/` to see how tiles and entities are defined.

## Algorithms

The game supports running search algorithms to solve levels automatically, such as:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform Cost Search (UCS)
- Hill Climbing (improved version to win the game)
- A* Search


## Screenshots

![Level 1](/screenshots/level1.png)

![Level 7](/screenshots/level7.png)

![Level 15](/screenshots/level15.png)

![level 7 - In Game](/screenshots/level7playing.png)

## Project structure (high-level)

```
lava_and_aqua_game/
├─ algorithms/        # pathfinding / solver implementations
├─ game_renderer/     # rendering code
├─ levels/            # level definitions
├─ screenshots/       # screenshots
├─ main.py            # program entrypoint
├─ game_engine.py     # core game loop and logic
├─ player_mode.py     # manual player controls
├─ algorithm_mode.py  # run algorithms / AI
└─ element.py         # tile / entity definitions
```
