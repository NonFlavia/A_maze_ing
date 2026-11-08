from collections import deque

from mazegen.errors import MazeError
from mazegen.grid import Grid

Position = tuple[int, int]


def open_neighbors(grid: Grid, position: Position) -> list[Position]:
    """Restituisce le celle raggiungibili direttamente da position."""
    x, y = position
    cell = grid.get_cell(x, y)
    neighbors: list[Position] = []

    if not cell.north and y > 0:
        neighbors.append((x, y - 1))
    if not cell.east and x < grid.width - 1:
        neighbors.append((x + 1, y))
    if not cell.south and y < grid.height - 1:
        neighbors.append((x, y + 1))
    if not cell.west and x > 0:
        neighbors.append((x - 1, y))

    walkable_neighbors: list[Position] = []
    for neighbor in neighbors:
        neighbor_x, neighbor_y = neighbor
        next_cell = grid.get_cell(neighbor_x, neighbor_y)
        if next_cell.is_walkable():
            walkable_neighbors.append(neighbor)
    return walkable_neighbors


def find_shortest_path(
    grid: Grid,
    entry: Position,
    exit_position: Position
) -> list[Position]:
    """Trova il percorso piu' corto con una ricerca BFS."""
    queue: deque[Position] = deque([entry])
    parents: dict[Position, Position | None] = {entry: None}

    while queue:
        current: Position = queue.popleft()
        if current == exit_position:
            break

        neighbors: list[Position] = open_neighbors(grid, current)
        for neighbor in neighbors:
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)

    if exit_position not in parents:
        raise MazeError("No valid path exists between ENTRY and EXIT")

    path: list[Position] = []
    position: Position | None = exit_position
    while position is not None:
        path.append(position)
        position = parents[position]
    path.reverse()
    return path


def path_to_directions(path: list[Position]) -> str:
    """Converte un percorso in una sequenza di N, E, S e W."""
    directions: list[str] = []

    for index in range(len(path) - 1):
        current_x, current_y = path[index]
        next_x, next_y = path[index + 1]
        movement: Position = (
            next_x - current_x,
            next_y - current_y,
        )

        if movement == (0, -1):
            directions.append("N")
        elif movement == (1, 0):
            directions.append("E")
        elif movement == (0, 1):
            directions.append("S")
        elif movement == (-1, 0):
            directions.append("W")
        else:
            raise MazeError("The solution contains non-adjacent cells")

    return "".join(directions)
