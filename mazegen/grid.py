import abc

from mazegen.cell import Cell, ClosedCell, NormalCell
from mazegen.errors import InvalidPositionError

Position = tuple[int, int]
RESET_COLOR: str = "\033[0m"


class Line(abc.ABC):
    """Base comune per una linea di celle.

    Per ora l'unica sottoclasse e' Row: questa classe astratta serve
    a tenere separato "cos'e' una linea di celle" da "come Row
    decide di riempirla"."""

    def __init__(self) -> None:
        """Crea la lista vuota cells della linea."""
        self.cells: list[Cell] = []

    @abc.abstractmethod
    def create_cells(self) -> None:
        """Popola self.cells."""
        pass


class Row(Line):
    """Una riga orizzontale della griglia, alla coordinata y
    indicata, lunga width celle."""

    def __init__(self, y: int, width: int) -> None:
        """Salva y e width e crea subito le celle della riga."""
        super().__init__()
        self.y: int = y
        self.width: int = width
        self.create_cells()

    def create_cells(self) -> None:
        """Crea width NormalCell, tutte con la stessa y."""
        for x in range(self.width):
            cell: NormalCell = NormalCell(x, self.y)
            self.cells.append(cell)


class Grid:
    """La griglia completa: una lista di Row, una per ogni valore di
    y da 0 a height-1."""

    def __init__(self, width: int, height: int) -> None:
        """Salva width e height e crea tutte le righe."""
        self.width: int = width
        self.height: int = height
        self.rows: list[Row] = []
        self.create_rows()

    def create_rows(self) -> None:
        """Crea height righe, ciascuna larga width celle."""
        for y in range(self.height):
            row: Row = Row(y, self.width)
            self.rows.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        """Risponde a: qual e' la cella alle coordinate x, y?

        Solleva InvalidPositionError se x o y sono fuori dai limiti
        della griglia."""
        if not (0 <= x < self.width):
            raise InvalidPositionError("Invalid x coordinate")
        if not (0 <= y < self.height):
            raise InvalidPositionError("Invalid y coordinate")
        return self.rows[y].cells[x]

    def close_cell(self, x: int, y: int) -> None:
        """Sostituisce la cella indicata con una ClosedCell."""
        self.get_cell(x, y)
        self.rows[y].cells[x] = ClosedCell(x, y)


# change_wall NON decide quali celle collegare: quella scelta spetta
# all'algoritmo di generazione, che sceglie due celle vicine e chiama
# questa funzione per aprire o chiudere il muro condiviso.
#
# closed=True  -> il muro resta/diventa chiuso
# closed=False -> il muro viene aperto (passaggio libero)
def change_wall(current: Cell, next_cell: Cell, closed: bool) -> None:
    """Imposta a closed il muro condiviso da current e next_cell.

    Le due celle devono essere adiacenti (differire di 1 su un solo
    asse), altrimenti viene sollevato InvalidPositionError. Il muro
    viene aggiornato su entrambe le celle, cosi' che i due lati
    restino sempre coerenti tra loro."""
    direction: tuple[int, int] = (
        next_cell.x - current.x, next_cell.y - current.y
    )

    match direction:
        case (1, 0):
            current.east, next_cell.west = closed, closed
        case (-1, 0):
            current.west, next_cell.east = closed, closed
        case (0, 1):
            current.south, next_cell.north = closed, closed
        case (0, -1):
            current.north, next_cell.south = closed, closed
        case _:
            raise InvalidPositionError("Cells are not adjacent")


def color_wall(text: str, wall_color: str) -> str:
    """Aggiunge un colore ANSI a una parte di parete."""
    if not wall_color:
        return text
    return f"{wall_color}{text}{RESET_COLOR}"


def print_north_walls(row: Row, wall_color: str) -> None:
    """Stampa la parete north di ogni cella della riga."""
    for cell in row.cells:
        wall: str = "   "
        if cell.north:
            wall = "---"
        print(color_wall("+", wall_color), end="")
        print(color_wall(wall, wall_color), end="")
    print(color_wall("+", wall_color))


def print_south_walls(row: Row, wall_color: str) -> None:
    """Stampa la parete south di ogni cella della riga.

    Va chiamata una sola volta, sull'ultima riga della griglia, per
    chiudere graficamente il fondo del labirinto."""
    for cell in row.cells:
        wall: str = "   "
        if cell.south:
            wall = "---"
        print(color_wall("+", wall_color), end="")
        print(color_wall(wall, wall_color), end="")
    print(color_wall("+", wall_color))


def cell_content(
    cell: Cell,
    entry: Position,
    exit_position: Position,
    path: set[Position]
) -> str:
    """Restituisce i tre caratteri mostrati dentro una cella."""
    position: Position = (cell.x, cell.y)
    if position == entry:
        return " E "
    if position == exit_position:
        return " X "
    if isinstance(cell, ClosedCell):
        return "###"
    if position in path:
        return " . "
    return "   "


def print_side_walls(
    row: Row,
    entry: Position,
    exit_position: Position,
    path: set[Position],
    wall_color: str
) -> None:
    """Stampa la parete west di ogni cella e, alla fine della riga,
    la parete east dell'ultima cella."""
    for cell in row.cells:
        west_wall: str = " "
        if cell.west:
            west_wall = "|"
        print(color_wall(west_wall, wall_color), end="")
        print(cell_content(cell, entry, exit_position, path), end="")

    east_wall: str = " "
    if row.cells[-1].east:
        east_wall = "|"
    print(color_wall(east_wall, wall_color))


def print_grid(
    grid: Grid,
    entry: Position,
    exit_position: Position,
    path: list[Position] | None = None,
    wall_color: str = ""
) -> None:
    """Stampa l'intera griglia in ASCII, riga per riga."""
    path_positions: set[Position] = set()
    if path is not None:
        for position in path:
            path_positions.add(position)

    for row in grid.rows:
        print_north_walls(row, wall_color)
        print_side_walls(
            row,
            entry,
            exit_position,
            path_positions,
            wall_color,
        )
    print_south_walls(grid.rows[-1], wall_color)
