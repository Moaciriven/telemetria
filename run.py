import subprocess
import os
import sys
import time
import threading
import psutil
import signal

def start_process(command, name):
    """Inicia um processo e retorna o objeto Popen com nome identificador"""
    print(f"[SISTEMA] Iniciando {name}...")
    try:
        return subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0), name
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar {name}: {str(e)}")
        return None, name

def monitor_system():
    """Monitora o uso de recursos do sistema em segundo plano"""
    while True:
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            print(f"[MONITOR] CPU: {cpu}% | MEM: {mem}%")
        except:
            pass
        time.sleep(10)

def main():
    # Verifica o modo de operação
    MODO_TESTE = "--teste" in sys.argv
    
    # Cria diretório de dados se necessário
    os.makedirs("data", exist_ok=True)
    
    processes = []
    
    try:
        print("""
        ###############################################
        #  SISTEMA DE TELEMETRIA PARA FOGUETE PET     #
        #  Iniciando todos os componentes...          #
        #  Modo: {}                         #
        ###############################################
        """.format("TESTE" if MODO_TESTE else "DEFINITIVO"))
        
        # Inicia monitoramento de recursos em thread separada
        monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        monitor_thread.start()
        
        # Comandos para iniciar os processos
        commands = {
            "SIMULADOR": "python src/simulador.py",
            "UDP_GETTER": f"python src/udp_getter.py {'--teste' if MODO_TESTE else ''}",
            "VISUALIZADOR": "python src/visualizador.py",
            "DASHBOARD": "streamlit run src/dashboard.py"
        }
        
        # Inicia os processos principais
        for name, cmd in commands.items():
            p, pname = start_process(cmd, name)
            if p:
                processes.append((p, pname))
            time.sleep(1)  # Intervalo entre inícios
        
        print("\n[SISTEMA] Todos os componentes iniciados!")
        print("[SISTEMA] Acesse o dashboard em: http://localhost:8501")
        print("[SISTEMA] Pressione CTRL+C para encerrar\n")
        
        # Verificação periódica de processos
        while True:
            active_processes = []
            for i, (p, name) in enumerate(processes):
                if p is None:
                    continue
                    
                status = p.poll()
                if status is None:
                    # Processo ainda está ativo
                    active_processes.append((p, name))
                else:
                    # Processo terminou - reinicia se for importante
                    if name not in ["SIMULADOR", "UDP_GETTER"] or not MODO_TESTE:
                        print(f"[SISTEMA] {name} terminou com código {status}. Reiniciando...")
                        new_p, new_name = start_process(commands[name], name)
                        if new_p:
                            active_processes.append((new_p, new_name))
                        else:
                            print(f"[ERRO] Falha ao reiniciar {name}")
                    else:
                        print(f"[SISTEMA] {name} terminou (modo teste)")
            
            processes = active_processes
            status_str = " | ".join([f"{name}: {'ATIVO' if p.poll() is None else 'INATIVO'}" for p, name in processes])
            print(status_str, end='\r')
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n[SISTEMA] Encerrando todos os processos...")
        for p, name in processes:
            if p and p.poll() is None:
                try:
                    # Método multiplataforma para encerrar
                    if os.name == 'nt':
                        p.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        p.terminate()
                    
                    # Espera o processo terminar
                    try:
                        p.wait(timeout=5)
                        print(f"[SISTEMA] {name} encerrado")
                    except subprocess.TimeoutExpired:
                        print(f"[ERRO] {name} não respondeu, terminando forçadamente")
                        p.kill()
                except Exception as e:
                    print(f"[ERRO] Falha ao encerrar {name}: {str(e)}")
        
        print("[SISTEMA] Todos os processos encerrados. Até logo!")
        sys.exit(0)

if __name__ == "__main__":
    # Verifica se está no ambiente virtual
    if not hasattr(sys, 'real_prefix') and 'VIRTUAL_ENV' not in os.environ:
        print("AVISO: Não está em um ambiente virtual. Recomendado executar com venv ativado")
    
    main()