## Nástroj pro barvení grafů s využitím genetického algoritmu

### Závislosti
Hlavní závislosti jsou DEAP a NetworkX, kompletní závislosti včetně jejich 
verzí jsou součástí souboru requirement.txt. Program byl provozován ve v Python
verze 3.10.1, kompatibilita s ostatními verzemi není zaručena, ale mělo by to fungovat
na všech verzích, kde jsou dostupné správné verze balíčků z requirements.

### Instalace
```
python -m venv .venv
. .venb/bin/activate
pip install -r requirements.txt
```

### Spuštění
Projekt má jen jeden volitelný argument -i, kterým je možné specifikovat cestu ke vstupnímu
souboru s grafem ve formátu graphml. V případě, argument není specifikován, použije se graf
DSJC125.1
```
python main.py [-i input_path]
```

Např:
```
python main.py -i DSJR500.1.graphml
```
