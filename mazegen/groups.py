Position = tuple[int, int]


def make_groups(positions: list[Position]) -> dict[Position, Position]:
    """Risponde a: qual e' lo stato iniziale dei gruppi?

    All'inizio ogni cella e' il rappresentante del proprio gruppo,
    da sola."""
    groups: dict[Position, Position] = {}
    for position in positions:
        groups[position] = position
    return groups


def find_group(
    groups: dict[Position, Position],
    position: Position
) -> Position:
    """Risponde a: chi rappresenta il gruppo di questa cella?

    Segue la catena finche' non trova una cella che rappresenta se
    stessa: quella e' il rappresentante dell'intero gruppo."""
    while groups[position] != position:
        position = groups[position]
    return position


def union_groups(
    groups: dict[Position, Position],
    first: Position,
    second: Position
) -> bool:
    """Risponde a: unisce i gruppi di first e second, se sono diversi?

    Restituisce True se l'unione e' avvenuta (quindi vale la pena
    abbattere il muro tra le due celle), False se erano gia' nello
    stesso gruppo (il muro va lasciato chiuso, altrimenti si crea
    un ciclo)."""
    root_first: Position = find_group(groups, first)
    root_second: Position = find_group(groups, second)
    if root_first == root_second:
        return False
    groups[root_first] = root_second
    return True
