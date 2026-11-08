from mazegen.grid import Grid

# Poche costanti con nome, invece di numeri "magici" sparsi nel
# codice: se domani cambi la forma delle cifre o il margine, basta
# toccare questi valori, il resto si ricalcola da solo.
DIGIT_WIDTH: int = 5
DIGIT_HEIGHT: int = 7
DIGIT_GAP: int = 1  # colonne libere tra il "4" e il "2"
MARGIN: int = 1  # celle libere minime intorno al pattern

FOUR: list[str] = [
    "#...#",
    "#...#",
    "#...#",
    "#####",
    "....#",
    "....#",
    "....#",
]

TWO: list[str] = [
    "#####",
    "....#",
    "....#",
    "#####",
    "#....",
    "#....",
    "#####",
]

PATTERN_WIDTH: int = DIGIT_WIDTH * 2 + DIGIT_GAP
PATTERN_HEIGHT: int = DIGIT_HEIGHT

# +2*MARGIN e non +MARGIN: il margine serve su entrambi i lati di
# ogni dimensione (sinistra e destra, sopra e sotto).
MIN_WIDTH: int = PATTERN_WIDTH + 2 * MARGIN
MIN_HEIGHT: int = PATTERN_HEIGHT + 2 * MARGIN


def fits_pattern(grid_width: int, grid_height: int) -> bool:
    """Risponde a: il pattern "42" (con margine) ci sta in questa
    griglia?"""
    return grid_width >= MIN_WIDTH and grid_height >= MIN_HEIGHT


def pattern_offset(grid_width: int, grid_height: int) -> tuple[int, int]:
    """Risponde a: da quale cella (x, y) comincia il pattern, per
    restare centrato in una griglia grid_width x grid_height?"""
    offset_x: int = (grid_width - PATTERN_WIDTH) // 2
    offset_y: int = (grid_height - PATTERN_HEIGHT) // 2
    return offset_x, offset_y


def draw_digit(grid: Grid, digit: list[str], x0: int, y0: int) -> None:
    """Disegna una singola cifra (FOUR o TWO) nella griglia,
    a partire dall'angolo in alto a sinistra (x0, y0).

    Ogni "#" nel disegno diventa una ClosedCell alla coordinata
    corrispondente; ogni "." viene lasciato com'era (NormalCell)."""
    for row_index, row_text in enumerate(digit):
        for col_index, symbol in enumerate(row_text):
            if symbol == "#":
                x: int = x0 + col_index
                y: int = y0 + row_index
                grid.close_cell(x, y)


def draw_pattern(grid: Grid, offset_x: int, offset_y: int) -> None:
    """Disegna il pattern "42" completo (le due cifre) nella
    griglia, a partire dall'angolo (offset_x, offset_y)."""
    draw_digit(grid, FOUR, offset_x, offset_y)
    second_digit_x: int = offset_x + DIGIT_WIDTH + DIGIT_GAP
    draw_digit(grid, TWO, second_digit_x, offset_y)
