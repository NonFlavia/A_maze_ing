import abc


class Cell(abc.ABC):
    """Una cella con coordinate e quattro pareti.

    E' astratta: non va istanziata direttamente. Definisce solo i
    dati e il comportamento comuni a NormalCell e ClosedCell."""

    def __init__(self, x: int, y: int) -> None:
        """Salva x e y e imposta a True le quattro pareti."""
        self.x: int = x
        self.y: int = y
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True

    @abc.abstractmethod
    def is_walkable(self) -> bool:
        """Risponde a: questa cella puo' essere attraversata?"""
        pass


class NormalCell(Cell):
    """Cella normale: fa parte dei passaggi del labirinto."""

    def is_walkable(self) -> bool:
        """Una NormalCell e' sempre attraversabile."""
        return True


class ClosedCell(Cell):
    """Cella chiusa: disegna il "42" usando celle
    completamente isolate dal resto del labirinto."""

    def is_walkable(self) -> bool:
        """Una ClosedCell non e' mai attraversabile."""
        return False
