import random

from mazegen.errors import ConfigError
from mazegen.grid import Grid
from mazegen.kruskal import generate_maze
from mazegen.pattern import draw_pattern, fits_pattern, pattern_offset
from mazegen.solver import find_shortest_path, path_to_directions

Position = tuple[int, int]
REQUIRED_KEYS: tuple[str, ...] = (
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
)


def check_required_keys(config: dict[str, str]) -> None:
    """Controlla che tutte le chiavi obbligatorie siano presenti."""
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ConfigError(f"Missing configuration key: {key}")


def parse_int(config: dict[str, str], key: str) -> int:
    """Converte in intero il valore associato a key."""
    try:
        return int(config[key])
    except (KeyError, ValueError) as error:
        raise ConfigError(f"{key} must be an integer") from error


def parse_coordinate(config: dict[str, str], key: str) -> Position:
    """Converte una coordinata scritta nel formato x,y."""
    try:
        parts: list[str] = config[key].split(",")
        if len(parts) != 2:
            raise ValueError
        x: int = int(parts[0])
        y: int = int(parts[1])
        return x, y
    except (KeyError, ValueError) as error:
        raise ConfigError(f"{key} must use the x,y format") from error


def parse_perfect_flag(config: dict[str, str]) -> bool:
    """Converte PERFECT in True oppure False."""
    value: str = config["PERFECT"].lower()
    if value == "true":
        return True
    if value == "false":
        return False
    raise ConfigError("PERFECT must be true or false")


def create_seed(config: dict[str, str]) -> int:
    """Legge SEED oppure ne crea uno casuale se non e' presente."""
    if "SEED" in config:
        return parse_int(config, "SEED")
    generator: random.SystemRandom = random.SystemRandom()
    return generator.randint(0, 2**32 - 1)


class MazeGen:
    """Genera e risolve un labirinto configurabile con Kruskal."""

    def __init__(self, config: dict[str, str]) -> None:
        """Converte, valida e salva i valori della configurazione."""
        check_required_keys(config)
        self.width: int = parse_int(config, "WIDTH")
        self.height: int = parse_int(config, "HEIGHT")
        self.entry: Position = parse_coordinate(config, "ENTRY")
        self.exit: Position = parse_coordinate(config, "EXIT")
        self.output_file: str = config["OUTPUT_FILE"]
        self.perfect: bool = parse_perfect_flag(config)
        self.seed: int = create_seed(config)
        self._validate_values()
        self.grid: Grid = Grid(self.width, self.height)
        self.generate()

    def _validate_values(self) -> None:
        """Controlla dimensioni, coordinate e nome del file."""
        if self.width <= 0 or self.height <= 0:
            raise ConfigError("WIDTH and HEIGHT must be positive")
        if not self._position_is_inside(self.entry):
            raise ConfigError("ENTRY is outside the maze")
        if not self._position_is_inside(self.exit):
            raise ConfigError("EXIT is outside the maze")
        if self.entry == self.exit:
            raise ConfigError("ENTRY and EXIT must be different")
        if not self.output_file.strip():
            raise ConfigError("OUTPUT_FILE cannot be empty")

    def _position_is_inside(self, position: Position) -> bool:
        """Controlla se una posizione appartiene alla griglia."""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def _draw_pattern_if_it_fits(self) -> None:
        """Disegna il 42 oppure segnala che la griglia e' piccola."""
        if not fits_pattern(self.width, self.height):
            print("Error: grid too small for the 42 pattern; continuing")
            return
        offset_x, offset_y = pattern_offset(self.width, self.height)
        draw_pattern(self.grid, offset_x, offset_y)

    def _validate_special_cells(self) -> None:
        """Controlla che entrata e uscita non siano dentro il 42."""
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        entry_cell = self.grid.get_cell(entry_x, entry_y)
        exit_cell = self.grid.get_cell(exit_x, exit_y)
        if not entry_cell.is_walkable():
            raise ConfigError("ENTRY overlaps the 42 pattern")
        if not exit_cell.is_walkable():
            raise ConfigError("EXIT overlaps the 42 pattern")

    def generate(self, seed: int | None = None) -> Grid:
        """Genera una nuova griglia usando il seed indicato."""
        if seed is not None:
            self.seed = seed
        self.grid = Grid(self.width, self.height)
        self._draw_pattern_if_it_fits()
        self._validate_special_cells()
        generate_maze(
            self.grid,
            self.seed,
            self.perfect,
            self.entry,
            self.exit,
        )
        return self.grid

    def get_solution(self) -> list[Position]:
        """Restituisce il percorso piu' corto da entry a exit."""
        return find_shortest_path(self.grid, self.entry, self.exit)

    def get_solution_directions(self) -> str:
        """Restituisce il percorso come lettere N, E, S e W."""
        solution: list[Position] = self.get_solution()
        return path_to_directions(solution)
