VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
TESTER = tester.py

.DEFAULT: help

help:
	@echo "make run"
	@echo "       run main script"
	@echo "make create_venv"
	@echo "       creates venv"
	@echo "make update_req"
	@echo "       updates requirements.txt"
	@echo "make clean"
	@echo "       cleans up downloaded files and venv"
	@echo "make clean_venv"
	@echo "       cleans up downloaded files and venv"

#run script
run:
	$(PYTHON) $(TESTER)

update_req:
	pip freeze > requirements.txt

create_venv:
	python3 -m venv $(VENV)

clean_venv:
	rm -rf $(VENV)

clean: clean_venv
	rm -rf data