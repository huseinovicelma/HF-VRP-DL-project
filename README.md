# HF-VRP-DL-project

## Descrizione
Questo progetto implementa il problema di ottimizzazione HF-VRP-DL (Heterogeneous Fleet Vehicle Routing Problem with Draft Limits), un problema di routing di veicoli con flotta eterogenea e limiti di pescaggio.

## Struttura del Progetto
- **dataset/**: Contiene le istanze del problema divise per dimensione e caratteristiche
  - Le cartelle sono organizzate secondo il formato `r_X_Y_Z_W` dove:
    - X: numero di porti
    - Y, Z, W: parametri specifici dell'istanza
- **src/**: Contiene il codice sorgente
  - `model.py`: Implementazione del modello matematico con Gurobi
  - `parse.py`: Funzioni per il parsing delle istanze
  - `utils.py`: Funzioni di utilità
  - `heuristics.py`: Implementazione di euristiche
  - `valid_inequalities.py`: Disuguaglianze valide per migliorare il modello
- **references/**: Contiene il paper di riferimento (HF-VRP-DL.pdf)
- **results/**: Contiene i risultati delle esecuzioni
- **test.py**: Script per testare il modello
- **scalability.py**: Script per analizzare la scalabilità del modello

## Come Utilizzare
1. Installare le dipendenze necessarie (Gurobi, Python)
2. Eseguire `test.py` per testare il modello su istanze specifiche
3. Utilizzare `scalability.py` per eseguire il modello su tutte le istanze presenti nella cartella `dataset/`

## Problema HF-VRP-DL
Il problema riguarda la pianificazione ottimale di rotte per una flotta eterogenea di navi che devono servire un insieme di porti, rispettando vincoli di capacità e limiti di pescaggio. L'obiettivo è minimizzare il costo totale di trasporto.