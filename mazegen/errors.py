class MazeError(Exception):
    """Errore base del progetto.

    Tutte le altre eccezioni derivano da questa, cosi' chi chiama il
    codice puo' scegliere se distinguere il tipo esatto di errore
    oppure catturare semplicemente MazeError."""
    pass


class ConfigError(MazeError):
    """Errore nel file di configurazione: chiave mancante, valore
    non valido, sintassi sbagliata, e simili."""
    pass


class InvalidPositionError(MazeError):
    """Errore relativo a una coordinata (x, y): fuori dai limiti
    della griglia, oppure due celle non adiacenti passate a una
    funzione che si aspetta celle vicine."""
    pass
