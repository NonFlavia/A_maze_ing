import sys

from mazegen.errors import ConfigError


def parse_config_line(raw_line: str) -> tuple[str, str] | None:
    """Risponde a: questa riga del file e' una coppia KEY=VALUE?

    Restituisce None per le righe da ignorare (vuote o commenti).
    Solleva ConfigError se la riga non e' vuota/commento ma non
    contiene un "=" ."""
    line: str = raw_line.strip()

    if not line or line.startswith("#"):
        return None

    if "=" not in line:
        raise ConfigError("Expected KEY=VALUE")

    key, value = line.split("=", 1)
    key = key.strip().upper()
    value = value.strip()

    if not key or not value:
        raise ConfigError("Configuration keys and values cannot be empty")

    return key, value


def read_config() -> dict[str, str]:
    """Risponde a: quali sono le coppie KEY=VALUE nel file passato
    da terminale?

    Solleva ConfigError se gli argomenti sono sbagliati o se il
    file non puo' essere aperto."""
    if len(sys.argv) != 2:
        raise ConfigError("Usage: python3 a_maze_ing.py config.txt")

    filename: str = sys.argv[1]
    content: dict[str, str] = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for raw_line in file:
                parsed_line: tuple[str, str] | None
                parsed_line = parse_config_line(raw_line)
                if parsed_line is not None:
                    key, value = parsed_line
                    if key in content:
                        raise ConfigError(f"Duplicated key: {key}")
                    content[key] = value
    except OSError as error:
        raise ConfigError(f"Cannot read configuration: {error}") from error

    if not content:
        raise ConfigError("The configuration file is empty")

    return content
