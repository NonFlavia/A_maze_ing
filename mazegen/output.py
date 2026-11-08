from mazegen.cell import Cell
from mazegen.errors import MazeError
from mazegen.grid import Grid, Row


def cell_to_hex(cell: Cell) -> str:
    """Risponde a: qual e' la cifra esadecimale che rappresenta le
    quattro pareti di questa cella?

    Bit usati: nord=1, est=2, sud=4, ovest=8. Una parete chiusa
    imposta il bit corrispondente."""
    value: int = 0
    if cell.north:
        value += 1
    if cell.east:
        value += 2
    if cell.south:
        value += 4
    if cell.west:
        value += 8
    return format(value, "X")


def row_to_hex(row: Row) -> str:
    """Risponde a: qual e' la stringa esadecimale che rappresenta
    tutte le celle di questa riga, nell'ordine?"""
    values: list[str] = []
    for cell in row.cells:
        hexadecimal_value: str = cell_to_hex(cell)
        values.append(hexadecimal_value)
    return "".join(values)


def write_output(
    grid: Grid,
    output_file: str,
    entry: tuple[int, int],
    exit_position: tuple[int, int],
    path: str
) -> None:
    """Scrive grid, entry, exit_position e path dentro output_file.

    Formato: una riga per ogni riga della griglia, poi una riga
    vuota, poi le coordinate di entry, poi quelle di exit_position,
    infine il percorso come sequenza di lettere N/E/S/W."""
    entry_x, entry_y = entry
    exit_x, exit_y = exit_position

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            for row in grid.rows:
                hexadecimal_row: str = row_to_hex(row)
                file.write(f"{hexadecimal_row}\n")
            file.write("\n")
            file.write(f"{entry_x},{entry_y}\n")
            file.write(f"{exit_x},{exit_y}\n")
            file.write(f"{path}\n")
    except OSError as error:
        raise MazeError(f"Cannot write output file: {error}") from error
