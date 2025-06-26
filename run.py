import subprocess
import os
import sys
import time
import threading
import psutil
import signal
import socket
from datetime import datetime

# ======== Configurações Globais ========
PORT_UDP = 5555
DASHBOARD_PORT = 8501
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "dados.csv")
STATUS_UPDATE_INTERVAL = 30  # segundos entre atualizações de status

# ======== Funções Utilitárias ========

def timestamp() -> str:
    """Retorna um timestamp formatado para os logs"""
    return datetime.now().strftime("%H:%M:%S")

def is_port_in_use(port: int) -> bool:
    """Verifica se uma porta está em uso"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_port(port: int, timeout: int = 10):
    """Aguarda até que uma porta esteja liberada"""
    print(f"[{timestamp()}] [SISTEMA] Verificando porta {port}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not is_port_in_use(port):
            return True
        time.sleep(0.5)
    return False

def clean_data_directory():
    """Remove o CSV anterior e garante diretório de dados"""
    print(f"[{timestamp()}] [SISTEMA] Preparando ambiente para novo lançamento...")
    if os.path.exists(CSV_PATH):
        try:
            os.remove(CSV_PATH)
            print(f"[{timestamp()}] [SISTEMA] Arquivo anterior removido: {CSV_PATH}")
        except Exception as e:
            print(f"[{timestamp()}] [ERRO] Falha ao remover arquivo: {str(e)}")
    os.makedirs(DATA_DIR, exist_ok=True)

def print_status(processes):
    """Mostra o status de todos os subprocessos"""
    status_list = []
    for p, name in processes:
        status = "ATIVO" if p and p.poll() is None else "INATIVO"
        status_list.append(f"{name}: {status}")
    print(f"[{timestamp()}] [STATUS] {' | '.join(status_list)}")

# ======== Monitoramento ========

def monitor_system():
    """Monitora uso de CPU e memória"""
    global monitoring_active
    while monitoring_active:
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            print(f"[{timestamp()}] [MONITOR] CPU: {cpu}% | MEM: {mem}%")
        except Exception:
            pass
        time.sleep(10)

# ======== Subprocessos ========

def start_process(command: str, name: str, dependencies: list = None) -> tuple:
    """Inicia subprocesso, verificando dependências"""
    if dependencies:
        print(f"[{timestamp()}] [INICIO] Verificando dependências para {name}: {', '.join(dependencies)}")
        for dep in dependencies:
            if not any(pname == dep for _, pname in processes):
                print(f"[{timestamp()}] [ERRO] Dependência não atendida para {name}: {dep}")
                return None, name

    print(f"[{timestamp()}] [SISTEMA] Iniciando {name}...")
    try:
        flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=flags), name
    except Exception as e:
        print(f"[{timestamp()}] [ERRO] Falha ao iniciar {name}: {str(e)}")
        return None, name

# ======== Função Principal ========

def main():
    global monitoring_active, processes

    MODO_TESTE = "--teste" in sys.argv
    monitoring_active = True
    processes = []
    last_status_print = 0

    print(f"""
    ###############################################
    #  SISTEMA DE TELEMETRIA PARA FOGUETE PET     #
    #  Iniciando todos os componentes...          #
    #  Modo: {'TESTE                              #' if MODO_TESTE else 'DEFINITIVO                         #'} 
    ###############################################
    """)

    if MODO_TESTE:
        clean_data_directory()

    # Inicia thread de monitoramento
    monitor_thread = threading.Thread(target=monitor_system, daemon=True)
    monitor_thread.start()

    # Comandos dos componentes (atualizados para nova estrutura)
    commands = {
        "UDP_GETTER": f"{sys.executable} src/udp_getter.py {'--teste' if MODO_TESTE else ''}",
        # Visualizador temporariamente desativado
        # "VISUALIZADOR": f"QT_QPA_PLATFORM=xcb {sys.executable} src/visualizador.py",
        "DASHBOARD": (
            f"{sys.executable} -m streamlit run src/app.py "
            f"--server.port {DASHBOARD_PORT} "
            "--server.headless true "
            "--global.showWarningOnDirectExecution false"
        ),
        "SIMULADOR": f"{sys.executable} src/simulador.py",
        "VISUALIZADOR": f"{sys.executable} src/visualizador.py"
    }

    # Ordem de inicialização e dependências
    startup_order = [
        ("UDP_GETTER", []),
        ("DASHBOARD", ["UDP_GETTER"]),
        ("SIMULADOR", ["UDP_GETTER"]),
        ("VISUALIZADOR", [])
    ]

    # Verifica se portas estão livres
    if is_port_in_use(PORT_UDP):
        print(f"[{timestamp()}] [ERRO] Porta UDP {PORT_UDP} já está em uso!")
        sys.exit(1)
    if is_port_in_use(DASHBOARD_PORT):
        print(f"[{timestamp()}] [ERRO] Porta do Dashboard {DASHBOARD_PORT} já está em uso!")
        sys.exit(1)

    # Inicializa subprocessos
    for name, deps in startup_order:
        cmd = commands[name]
        p, pname = start_process(cmd, name, dependencies=deps)
        if p:
            processes.append((p, pname))
            if name == "UDP_GETTER":
                print(f"[{timestamp()}] [SISTEMA] Aguardando inicialização do UDP_GETTER...")
                time.sleep(2)
            elif name == "DASHBOARD":
                print(f"[{timestamp()}] [SISTEMA] Aguardando inicialização do Dashboard...")
                time.sleep(5)  # Mais tempo para o Streamlit iniciar
            else:
                time.sleep(1)

    print(f"\n[{timestamp()}] [SISTEMA] Todos os componentes iniciados!")
    print(f"[{timestamp()}] [SISTEMA] Acesse: http://localhost:{DASHBOARD_PORT}")
    print(f"[{timestamp()}] [SISTEMA] Pressione CTRL+C para encerrar\n")

    print_status(processes)
    last_status_print = time.time()

    # Loop principal de verificação
    try:
        while True:
            active_processes = []
            status_changed = False

            for p, name in processes:
                if p is None:
                    continue

                if p.poll() is None:
                    # Processo ainda está rodando
                    active_processes.append((p, name))
                else:
                    # Processo terminou
                    if name == "SIMULADOR":
                        # Simulador finalizado - não reiniciamos
                        print(f"[{timestamp()}] [SISTEMA] SIMULADOR finalizado. Não será reiniciado.")
                        continue
                    else:
                        # Outros processos são reiniciados
                        print(f"[{timestamp()}] [SISTEMA] {name} finalizado, reiniciando...")
                        status_changed = True
                        new_p, _ = start_process(commands[name], name)
                        if new_p:
                            active_processes.append((new_p, name))

            processes = active_processes

            if status_changed or (time.time() - last_status_print) > STATUS_UPDATE_INTERVAL:
                print_status(processes)
                last_status_print = time.time()

            time.sleep(5)

    except KeyboardInterrupt:
        print(f"\n[{timestamp()}] [SISTEMA] Encerrando todos os processos...")
        monitoring_active = False
        for p, name in processes:
            if p and p.poll() is None:
                try:
                    if os.name == 'nt':
                        p.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        p.terminate()
                    try:
                        p.wait(timeout=3)
                        print(f"[{timestamp()}] [SISTEMA] {name} encerrado")
                    except subprocess.TimeoutExpired:
                        print(f"[{timestamp()}] [ERRO] Timeout ao encerrar {name}. Forçando...")
                        p.kill()
                except Exception as e:
                    print(f"[{timestamp()}] [ERRO] Falha ao encerrar {name}: {e}")
        print(f"[{timestamp()}] [SISTEMA] Todos os processos encerrados. Até logo!")
        sys.exit(0)

# ======== Execução ========

if __name__ == "__main__":
    if not hasattr(sys, 'real_prefix') and 'VIRTUAL_ENV' not in os.environ:
        print(f"[{timestamp()}] [AVISO] Recomendado executar com venv ativado")
    main()