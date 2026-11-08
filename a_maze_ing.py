from mazegen.config import read_config
from mazegen.errors import MazeError
from mazegen.grid import print_grid
from mazegen.maze import MazeGen
from mazegen.output import write_output

Position = tuple[int, int]
WALL_COLORS: list[tuple[str, str]] = [
    ("default", ""),
    ("cyan", "\033[96m"),
    ("yellow", "\033[93m"),
    ("magenta", "\033[95m"),
]


def save_maze(maze: MazeGen) -> None:
    """Salva griglia e soluzione nel file configurato."""
    directions: str = maze.get_solution_directions()
    write_output(
        maze.grid,
        maze.output_file,
        maze.entry,
        maze.exit,
        directions,
    )
    print(f"Output written to {maze.output_file}")


def show_maze(
    maze: MazeGen,
    show_path: bool,
    color_index: int,
    solution: list[Position]
) -> None:
    """Mostra il labirinto e le informazioni essenziali."""
    visible_path: list[Position] | None = None
    if show_path:
        visible_path = solution

    color_name, wall_color = WALL_COLORS[color_index]
    print()
    print_grid(
        maze.grid,
        maze.entry,
        maze.exit,
        visible_path,
        wall_color,
    )
    print(f"Seed: {maze.seed} | Wall color: {color_name}")
    print("E = entry | X = exit | ### = 42 | . = shortest path")


def run_interface(maze: MazeGen) -> None:
    """Gestisce le interazioni obbligatorie del terminale."""
    show_path: bool = False
    color_index: int = 0
    solution: list[Position] = maze.get_solution()
    save_maze(maze)

    while True:
        show_maze(maze, show_path, color_index, solution)
        print("R = regenerate | P = show/hide path | C = color | Q = quit")

        try:
            command: str = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if command == "q":
            return
        if command == "p":
            show_path = not show_path
        elif command == "c":
            color_index += 1
            if color_index == len(WALL_COLORS):
                color_index = 0
        elif command == "r":
            maze.generate(maze.seed + 1)
            solution = maze.get_solution()
            save_maze(maze)
        else:
            print("Unknown command")


def main() -> None:
    """Legge il config, genera il labirinto e avvia l'interfaccia."""
    try:
        config: dict[str, str] = read_config()
        maze: MazeGen = MazeGen(config)
        run_interface(maze)
    except MazeError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
