import socket
import csv
import os
import sys
from pathlib import Path
import time

# Verifica o modo de operação
MODO_TESTE = False
if len(sys.argv) > 1 and sys.argv[1] == "--teste":
    MODO_TESTE = True

UDP_PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

# Caminho para o arquivo CSV
dir_path = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(dir_path, "..", "data")
csv_path = os.path.join(data_dir, "dados.csv")

# Garante que o diretório existe
os.makedirs(data_dir, exist_ok=True)

# Modo teste: sobrescreve o arquivo
# Modo definitivo: adiciona ao arquivo existente
if MODO_TESTE:
    file_mode = "w"
else:
    file_mode = "a"

# Cria o arquivo se não existir ou se for modo teste
if MODO_TESTE or not os.path.exists(csv_path):
    with open(csv_path, file_mode, newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lat", "lon", "alt", "vel"])

print(f"[UDP] Aguardando dados na porta {UDP_PORT}...")
print(f"[UDP] Modo: {'TESTE (sobrescreve)' if MODO_TESTE else 'DEFINITIVO (acumula)'}")
print(f"[UDP] Salvando em: {csv_path}")

try:
    while True:
        data, _ = sock.recvfrom(1024)
        msg = data.decode().strip()
        
        # Se receber "END", encerra o getter no modo teste
        if msg == "END":
            if MODO_TESTE:
                print("[UDP] Recebido sinal de fim. Encerrando no modo teste.")
                break
            else:
                continue
            
        # Escreve no CSV
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(msg.split(','))
            print(f"[UDP] Dados salvos: {msg}")
            
except KeyboardInterrupt:
    print("\n[UDP] Interrompido pelo usuário.")
except Exception as e:
    print(f"[ERRO UDP] {str(e)}")
finally:
    sock.close()
    print("[UDP] Socket fechado.")