*This project has been created as part of the 42 curriculum by amgiunti, flavides.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and solver written in Python. The program reads a configuration file, generates a random maze, calculates the shortest path between the entrance and the exit, displays the result in the terminal, and saves it in hexadecimal format.

When the maze dimensions allow it, the maze contains a "42" made of completely closed cells. The project implements only the mandatory features: one generation algorithm, no animations, and no graphical interface.

## Instructions

Requirements:

- Python 3.10 or later;
- `make`;
- `pip` to install the checking tools and build the package.

Install the required tools:

```bash
make install
```

Run the program using the `config.txt` file:

```bash
make run
```

Run the program using another configuration file:

```bash
python3 a_maze_ing.py config_file.txt
```

Code checks:

```bash
make lint
make lint-strict
```

Build the reusable package:

```bash
make build
```

This command creates a `mazegen-*.whl` file in the project root directory.

## Interactive commands

- `R`: generate a new maze;
- `P`: show or hide the shortest path;
- `C`: change the wall color;
- `Q`: quit the program.

## Configuration file

The file uses one `KEY=VALUE` pair per line. Empty lines and lines starting with `#` are ignored. Keys can also be written in lowercase.

Mandatory keys:

- `WIDTH`: positive maze width;
- `HEIGHT`: positive maze height;
- `ENTRY`: entrance coordinates in `x,y` format;
- `EXIT`: exit coordinates in `x,y` format;
- `OUTPUT_FILE`: output file name or path;
- `PERFECT`: `True` for a perfect maze, `False` for a maze with at least one alternative path.

Optional key:

- `SEED`: an integer that makes maze generation reproducible. If it is missing, the program generates a random seed and displays it on screen.

Example:

```text
WIDTH=15
HEIGHT=9
ENTRY=0,0
EXIT=14,8
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

The program handles missing keys, malformed lines, invalid numbers, invalid boolean values, coordinates outside the grid, and coordinates overlapping the "42".

## Output file

The file contains:

1. `HEIGHT` hexadecimal rows containing `WIDTH` characters;
2. one empty line;
3. the `ENTRY` coordinates;
4. the `EXIT` coordinates;
5. the shortest path as a sequence of `N`, `E`, `S`, `W`.

Each cell uses four bits to represent closed walls:

- north = `1`;
- east = `2`;
- south = `4`;
- west = `8`.

## Maze algorithm

The project uses only the randomized Kruskal algorithm.

At the beginning, each walkable cell belongs to a separate group. The internal walls are shuffled using the seed. A wall is opened only when it connects two different groups, which are then merged.

This choice makes it easy to verify two requirements:

- all walkable cells belong to the same group;
- with `PERFECT=True`, no cycles are created, so there is only one path between every pair of cells.

The cells belonging to the "42" are not added to the groups and remain closed.

With `PERFECT=False`, only one wall rejected by Kruskal is opened, but the wall is not chosen randomly: the new cycle must create a second route between `ENTRY` and `EXIT`. Before confirming the opening, the program also checks that a completely open 3x3 area is not created.

## Shortest path

The shortest path is found using BFS. BFS visits reachable cells level by level and stores the parent of each cell. When it reaches `EXIT`, it reconstructs the path by moving backwards until it reaches `ENTRY`.

## Reusable module

The `mazegen` folder is a reusable Python package. After building and installing the `.whl` file, it can be used like this:

```python
from mazegen import MazeGen

config = {
    "WIDTH": "15",
    "HEIGHT": "9",
    "ENTRY": "0,0",
    "EXIT": "14,8",
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": "True",
    "SEED": "42",
}

maze = MazeGen(config)
grid = maze.grid
solution = maze.get_solution_directions()
```

Files related to the interactive visualization remain outside the package. The module contains the data structures, generation logic, solver, and output-writing logic.

## Team and project management

### Roles

- `amgiunti`: configuration, `Cell`/`Grid` structure, output, and program integration;
- `flavides`: groups, Kruskal algorithm, generation checks, and solver;
- shared work: interface, testing, documentation, and evaluation preparation.

### Planning and evolution

The initial plan divided the project by files. During development, it became more useful to divide it into small, testable behaviors: reading the configuration, building the grid, modifying a wall, generating, solving, saving, and finally displaying the maze.

The different parts were integrated one at a time and were also tested using small grids.

### What worked well

- short functions with one specific responsibility;
- frequent checks on shared walls and connectivity;
- comparison and discussion between both team members before integrating the main parts.

### What could be improved

- defining the interfaces between files earlier;
- preparing the configuration file edge cases earlier;
- spending more time on a shared explanation of the algorithm.

### Tools

Python, VS Code, Git/GitHub, and `pdb` were used during the project.

`flake8` and `mypy` are the tools required by the project to identify style issues and missing type annotations before submission.

## Resources

- Python documentation - `random`: reproducible wall shuffling using a seed;
- Python documentation - `collections.deque`: queue used by BFS;
- Python Packaging User Guide: `pyproject.toml` configuration and `.whl` file creation;
- documentation and educational material about Kruskal's algorithm and the union-find data structure.

Artificial intelligence was used as a learning support tool to break the subject down into smaller steps, discuss edge cases, check errors, and make the code easier to read.
