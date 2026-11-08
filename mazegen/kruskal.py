import random

from mazegen.errors import ConfigError, MazeError
from mazegen.grid import Grid, change_wall
from mazegen.groups import find_group, make_groups, union_groups
from mazegen.solver import find_shortest_path

Position = tuple[int, int]
Wall = tuple[Position, Position]
PathEdge = frozenset[Position]


def walkable_positions(grid: Grid) -> list[Position]:
    """Risponde a: quali celle della griglia sono attraversabili?

    Esclude le celle chiuse del pattern "42": quelle non devono mai
    entrare a far parte del labirinto generato."""
    positions: list[Position] = []
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.get_cell(x, y)
            if cell.is_walkable():
                positions.append((x, y))
    return positions


def walkable_internal_walls(grid: Grid) -> list[Wall]:
    """Risponde a: quali muri interni collegano due celle
    attraversabili?

    Un muro verso una cella chiusa (il "42") non viene mai preso in
    considerazione: cosi' quelle celle restano isolate, come vuole
    il subject, invece di essere agganciate per sbaglio al resto
    del labirinto."""
    walls: list[Wall] = []
    positions: list[Position] = walkable_positions(grid)
    for position in positions:
        x, y = position
        if x + 1 < grid.width and grid.get_cell(x + 1, y).is_walkable():
            walls.append(((x, y), (x + 1, y)))
        if y + 1 < grid.height and grid.get_cell(x, y + 1).is_walkable():
            walls.append(((x, y), (x, y + 1)))
    return walls


def change_wall_from_positions(
    grid: Grid,
    first: Position,
    second: Position,
    closed: bool
) -> None:
    """Cambia il muro condiviso dalle celle first e second."""
    first_x, first_y = first
    second_x, second_y = second
    first_cell = grid.get_cell(first_x, first_y)
    second_cell = grid.get_cell(second_x, second_y)
    change_wall(first_cell, second_cell, closed)


def block_is_fully_open(grid: Grid, start_x: int, start_y: int) -> bool:
    """Controlla se un blocco 3x3 non contiene muri interni."""
    for y in range(start_y, start_y + 3):
        for x in range(start_x, start_x + 2):
            cell = grid.get_cell(x, y)
            if cell.east:
                return False

    for y in range(start_y, start_y + 2):
        for x in range(start_x, start_x + 3):
            cell = grid.get_cell(x, y)
            if cell.south:
                return False

    return True


def has_open_3x3_area(grid: Grid) -> bool:
    """Controlla se nella griglia esiste un'area 3x3 aperta."""
    for y in range(grid.height - 2):
        for x in range(grid.width - 2):
            if block_is_fully_open(grid, x, y):
                return True
    return False


def check_connectivity(
    groups: dict[Position, Position],
    positions: list[Position]
) -> None:
    """Controlla che tutte le celle attraversabili siano unite."""
    if not positions:
        raise MazeError("The maze has no walkable cells")

    first_root: Position = find_group(groups, positions[0])
    for position in positions:
        current_root: Position = find_group(groups, position)
        if current_root != first_root:
            raise MazeError("The walkable maze area is not connected")


def path_edges(path: list[Position]) -> set[PathEdge]:
    """Converte un percorso nelle coppie di celle che attraversa."""
    edges: set[PathEdge] = set()
    for index in range(len(path) - 1):
        first: Position = path[index]
        second: Position = path[index + 1]
        edges.add(frozenset((first, second)))
    return edges


def wall_creates_alternative_solution(
    grid: Grid,
    first: Position,
    second: Position,
    solution_edges: set[PathEdge]
) -> bool:
    """Controlla se il nuovo ciclo tocca il percorso E-X.

    Prima di aprire il muro esiste un solo percorso tra first e
    second. Se quel percorso condivide un passaggio con la soluzione,
    il nuovo muro crea una seconda strada tra ENTRY ed EXIT."""
    cycle_path: list[Position]
    cycle_path = find_shortest_path(grid, first, second)
    cycle_edges: set[PathEdge] = path_edges(cycle_path)

    for edge in cycle_edges:
        if edge in solution_edges:
            return True
    return False


def open_extra_wall(
    grid: Grid,
    rejected_walls: list[Wall],
    entry: Position,
    exit_position: Position
) -> None:
    """Apre tutti i muri rifiutati che creano una strada alternativa
    tra ENTRY ed EXIT, senza mai creare un'area 3x3 aperta.

    Il percorso piu' corto viene ricalcolato ad ogni tentativo:
    aprire un muro puo' creare una scorciatoia che accorcia la
    soluzione, quindi il confronto deve restare aggiornato invece
    di usare sempre lo stesso percorso calcolato all'inizio."""
    opened_count: int = 0
    for first, second in rejected_walls:
        solution: list[Position] = find_shortest_path(
            grid, entry, exit_position
        )
        solution_edges: set[PathEdge] = path_edges(solution)

        creates_solution: bool = wall_creates_alternative_solution(
            grid,
            first,
            second,
            solution_edges,
        )
        if not creates_solution:
            continue

        change_wall_from_positions(grid, first, second, closed=False)
        if has_open_3x3_area(grid):
            change_wall_from_positions(grid, first, second, closed=True)
        else:
            opened_count += 1

    if opened_count == 0:
        raise ConfigError(
            "These dimensions cannot create a non-perfect maze"
        )


def generate_maze(
    grid: Grid,
    seed: int,
    perfect: bool,
    entry: Position,
    exit_position: Position
) -> None:
    """Genera un labirinto con Kruskal randomizzato.

    Mescola tutti i muri interni tra celle attraversabili e li
    scorre uno alla volta: un muro viene abbattuto solo se le due
    celle che separa non sono ancora nello stesso gruppo, cosi' da
    non creare cicli. Se perfect e' False, apre tutti i muri
    rifiutati che creano una strada alternativa tra entrata e
    uscita, non solo il primo."""
    walls: list[Wall] = walkable_internal_walls(grid)
    rng: random.Random = random.Random(seed)
    rng.shuffle(walls)

    positions: list[Position] = walkable_positions(grid)
    groups: dict[Position, Position] = make_groups(positions)
    rejected_walls: list[Wall] = []

    for position_a, position_b in walls:
        if union_groups(groups, position_a, position_b):
            change_wall_from_positions(
                grid, position_a, position_b, closed=False
            )
        else:
            rejected_walls.append((position_a, position_b))

    check_connectivity(groups, positions)

    if not perfect:
        rng.shuffle(rejected_walls)
        open_extra_wall(
            grid,
            rejected_walls,
            entry,
            exit_position,
        )
