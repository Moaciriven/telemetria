.PHONY: all venv clean run run_ht run_st run_sim analyze

VENV_DIR = venv
DATA_DIR = data
CSV_FILE = $(DATA_DIR)/dados.csv

ifeq ($(OS),Windows_NT)
    SHELL := powershell.exe
    .SHELLFLAGS := -NoProfile -Command
    RMDIR_CMD = Remove-Item -LiteralPath '$(subst /,\\,$1)' -Recurse -Force -ErrorAction SilentlyContinue
else
    SHELL := /bin/sh
    RMDIR_CMD = rm -rf $1 || true
endif

PYTHON := $(if $(filter Windows_NT,$(OS)),python,python3)
PYTHON_EXEC := $(if $(filter Windows_NT,$(OS)),$(VENV_DIR)\\Scripts\\python,$(VENV_DIR)/bin/python)
MKDIR_CMD := $(if $(filter Windows_NT,$(OS)),mkdir,$(if $(shell uname),mkdir -p))

all: venv $(CSV_FILE)

venv:
	@echo "Criando ambiente virtual..."
	@$(PYTHON) -m venv "$(VENV_DIR)"
	@echo "Instalando dependências..."
	@$(PYTHON_EXEC) -m pip install --upgrade pip
	@$(PYTHON_EXEC) -m pip install -r requirements.txt

$(CSV_FILE):
	@echo "Preparando arquivo CSV..."
	@mkdir -p "$(DATA_DIR)"
	@echo "lat,lon,alt,vel" > "$(CSV_FILE)"

run:
	@echo "Execute em 3 terminais separados:"
	@echo "Terminal 1: make run_ht"
	@echo "Terminal 2: make run_st"
	@echo "Terminal 3: make run_sim"

run_ht:
	@$(PYTHON_EXEC) src/hardtime_csv.py

run_st:
	@$(PYTHON_EXEC) src/udp_getter.py

run_sim:
	@$(PYTHON_EXEC) src/simulador.py

analyze:
	@echo "Analisando dados..."
	@$(PYTHON_EXEC) src/analyze.py

clean:
	@echo "Limpando pastas venv e data..."
	@$(call RMDIR_CMD,$(VENV_DIR))
	@$(call RMDIR_CMD,$(DATA_DIR))
	@echo "Pastas removidas."
