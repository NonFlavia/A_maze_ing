*This project has been created as part of the 42 curriculum by <amgiunti>, <flavides>.*

# A-Maze-ing

## Description

A-Maze-ing e' un generatore e risolutore di labirinti scritto in
Python. Il programma legge un file di configurazione, genera un
labirinto casuale, calcola il percorso piu' corto tra entrata e
uscita, mostra il risultato nel terminale e lo salva in formato
esadecimale.

Quando le dimensioni lo consentono, il labirinto contiene un "42"
formato da celle completamente chiuse. Il progetto implementa solo
le funzionalita' obbligatorie: un algoritmo di generazione, nessuna
animazione e nessuna interfaccia grafica.

## Instructions

Requisiti:

- Python 3.10 o successivo;
- `make`;
- `pip` per installare gli strumenti di controllo e creare il
  pacchetto.

Installazione degli strumenti:

```bash
make install
```

Avvio con il file `config.txt`:

```bash
make run
```

Avvio con un altro file di configurazione:

```bash
python3 a_maze_ing.py nome_config.txt
```

Controlli del codice:

```bash
make lint
make lint-strict
```

Creazione del pacchetto riutilizzabile:

```bash
make build
```

Il comando crea un file `mazegen-*.whl` nella cartella principale.

## Interactive commands

- `R`: genera un nuovo labirinto;
- `P`: mostra oppure nasconde il percorso piu' corto;
- `C`: cambia il colore delle pareti;
- `Q`: chiude il programma.

## Configuration file

Il file usa una coppia `KEY=VALUE` per riga. Le righe vuote e le
righe che iniziano con `#` vengono ignorate. Le chiavi possono
essere scritte anche in minuscolo.

Chiavi obbligatorie:

- `WIDTH`: larghezza positiva del labirinto;
- `HEIGHT`: altezza positiva del labirinto;
- `ENTRY`: coordinate dell'entrata nel formato `x,y`;
- `EXIT`: coordinate dell'uscita nel formato `x,y`;
- `OUTPUT_FILE`: nome o percorso del file di output;
- `PERFECT`: `True` per un labirinto perfetto, `False` per un
  labirinto con almeno un percorso alternativo.

Chiave facoltativa:

- `SEED`: numero intero che rende la generazione riproducibile. Se
  manca, il programma ne crea uno casuale e lo mostra a schermo.

Esempio:

```text
WIDTH=15
HEIGHT=9
ENTRY=0,0
EXIT=14,8
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

Il programma gestisce chiavi mancanti, righe malformate, numeri non
validi, booleani errati, coordinate fuori dalla griglia e
coordinate sovrapposte al "42".

## Output file

Il file contiene:

1. `HEIGHT` righe esadecimali di `WIDTH` caratteri;
2. una riga vuota;
3. le coordinate di `ENTRY`;
4. le coordinate di `EXIT`;
5. il percorso piu' corto come sequenza di `N`, `E`, `S`, `W`.

Ogni cella usa quattro bit per rappresentare le pareti chiuse:

- nord = `1`;
- est = `2`;
- sud = `4`;
- ovest = `8`.

## Maze algorithm

Il progetto usa soltanto l'algoritmo di Kruskal randomizzato.
All'inizio ogni cella attraversabile appartiene a un gruppo
separato. I muri interni vengono mescolati usando il seed. Un muro
viene aperto soltanto quando collega due gruppi diversi, che vengono
poi uniti.

Questa scelta rende semplice controllare due requisiti:

- tutte le celle attraversabili appartengono allo stesso gruppo;
- con `PERFECT=True` non vengono creati cicli e quindi esiste un
  solo percorso tra ogni coppia di celle.

Le celle del "42" non vengono inserite nei gruppi e restano chiuse.
Con `PERFECT=False` viene aperto un solo muro rifiutato da Kruskal,
ma non viene scelto un muro qualsiasi: il nuovo ciclo deve creare
una seconda strada tra `ENTRY` ed `EXIT`. Prima di confermare
l'apertura, il programma controlla anche che non appaia un'area 3x3
completamente aperta.

## Shortest path

Il percorso piu' corto viene trovato con BFS. BFS visita le celle
raggiungibili a livelli e salva il genitore di ogni cella. Quando
raggiunge `EXIT`, ricostruisce il percorso tornando indietro fino a
`ENTRY`.

## Reusable module

La cartella `mazegen` e' un pacchetto Python riutilizzabile. Dopo
aver creato e installato il file `.whl`, puo' essere usato cosi':

```python
from mazegen import MazeGen

config = {
    "WIDTH": "15",
    "HEIGHT": "9",
    "ENTRY": "0,0",
    "EXIT": "14,8",
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": "True",
    "SEED": "42",
}

maze = MazeGen(config)
grid = maze.grid
solution = maze.get_solution_directions()
```

I file relativi alla visualizzazione interattiva restano fuori dal
pacchetto. Il modulo contiene dati, generazione, soluzione e
scrittura dell'output.

## Team and project management

### Roles

- `<LOGIN_1>`: configurazione, struttura `Cell`/`Grid`, output e
  integrazione del programma;
- `<LOGIN_2>`: gruppi, algoritmo di Kruskal, controlli della
  generazione e solver;
- lavoro condiviso: interfaccia, test, documentazione e preparazione
  dell'evaluation.

### Planning and evolution

Il piano iniziale divideva il progetto per file. Durante lo
sviluppo e' diventato piu' utile dividerlo in piccoli comportamenti
verificabili: leggere il config, costruire la griglia, modificare un
muro, generare, risolvere, salvare e infine visualizzare. Le parti
sono state integrate una alla volta e provate anche su griglie
piccole.

### What worked well

- funzioni brevi con un compito preciso;
- controlli frequenti sui muri condivisi e sulla connettivita';
- confronto tra le due componenti del gruppo prima di integrare le
  parti principali.

### What could be improved

- definire prima le interfacce tra i file;
- preparare prima i casi limite del file di configurazione;
- dedicare piu' tempo alla spiegazione condivisa dell'algoritmo.

### Tools

Sono stati usati Python, VS Code, Git/GitHub e `pdb`. `flake8` e
`mypy` sono gli strumenti previsti dal progetto per individuare
errori di stile e annotazioni mancanti prima della consegna.

## Resources

- Python documentation - `random`: mescolamento riproducibile dei
  muri tramite seed;
- Python documentation - `collections.deque`: coda usata da BFS;
- Python Packaging User Guide: configurazione di `pyproject.toml` e
  creazione del file `.whl`;
- documentazione e materiale didattico su Kruskal e sulla struttura
  union-find.

L'intelligenza artificiale e' stata usata come supporto didattico
per tradurre il subject in passaggi piu' piccoli, discutere i casi
limite, controllare errori e rendere il codice piu' leggibile.