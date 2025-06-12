.PHONY: all venv clean run run_ht run_st run_sim analyze

# Diretórios e arquivos
VENV_DIR = venv
DATA_DIR = data
CSV_FILE = $(DATA_DIR)/dados.csv

# Detecta o sistema operacional
ifeq ($(OS),Windows_NT)
    PYTHON = python
    PYTHON_EXEC = $(VENV_DIR)\\Scripts\\python
    MKDIR = mkdir
    RMDIR = rmdir /s /q
    EXISTS = if exist
    NULL_OUT = > nul 2>&1
else
    PYTHON = python3
    PYTHON_EXEC = $(VENV_DIR)/bin/python
    MKDIR = mkdir -p
    RMDIR = rm -rf
    EXISTS = test -d
    NULL_OUT = > /dev/null 2>&1
endif

all: venv $(CSV_FILE)

venv:
	@echo "Criando ambiente virtual..."
	@$(PYTHON) -m venv "$(VENV_DIR)"
	@echo "Instalando dependências..."
	@$(PYTHON_EXEC) -m pip install --upgrade pip
	@$(PYTHON_EXEC) -m pip install -r requirements.txt

$(CSV_FILE):
	@echo "Preparando arquivo CSV..."
	@$(MKDIR) "$(DATA_DIR)"
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
	@-$(EXISTS) "$(VENV_DIR)" && $(RMDIR) "$(VENV_DIR)" $(NULL_OUT) || true
	@-$(EXISTS) "$(DATA_DIR)" && $(RMDIR) "$(DATA_DIR)" $(NULL_OUT) || true
	@echo "Pastas removidas."