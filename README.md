# Načtení a zobrazení přehledu o elektroencefalografických datových sadách s balíčkem MNE
Tento program složí k  zpracování a vizualizaci elektroencefalografických dat. Součástí programu je implementace pro 3 datové sady. 
Pokud si přejete vizualizovat vlastní datovou sadu je nutné implementovat si vlastní třídu dědíci z dataset.py - použijete šablonovou třídu datasetTemplate a implementujete potřebné metody.

## Ako spustiť projekt

- make create_venv
- source venv/bin/activate
- pip install -r requirements.txt
- ipython kernel install --user --name=venv
- make run OR jupyter lab

Po zpuštění jupyter notebooku visializer.ipynb, zvolte 'venv' kernel a pouštějte buňky a rozhraní vás již provede.

## Štruktúra projektu

  * src/ - zdrojové soubory projektu
  * data/ - datové soubory se kterými projekt pracuje
    * data/html/ - zdrojové soubory stránek ze kterých se stahujou datové soubory
    * data/raw_eeg_data - stáhnuté soubory jednotlivých datasetu
  * Makefile - pravidla pro vytvoreni virtualniho prostredi a spusteni projektu ze skriptu
  * visualizer.ipynb - notebook s rozhranim pro vizualizaci datových sad
  * tester.py - skript pro spusteni projektu z terminalu
  * README.md
  * requirements.txt - potrebne knihovny pro spusteni