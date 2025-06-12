import socket
import time
import random

UDP_IP = "127.0.0.1"  # Localhost, ajuste se precisar enviar para outro IP
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def generate_data():
    # Simula valores: lat, lon, alt, vel
    lat = random.uniform(-90.0, 90.0)
    lon = random.uniform(-180.0, 180.0)
    alt = random.uniform(0, 10000)       # altitude em metros
    vel = random.uniform(0, 300)         # velocidade em km/h
    return f"{lat:.6f},{lon:.6f},{alt:.2f},{vel:.2f}"

print(f"[SIM] Enviando dados para UDP {UDP_IP}:{UDP_PORT}... Pressione Ctrl+C para sair.")

try:
    while True:
        data = generate_data()
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
        print(f"[SIM] Enviado: {data}")
        time.sleep(0.1)  # envia a cada 100ms (10 vezes por segundo)
except KeyboardInterrupt:
    print("\n[SIM] Simulador finalizado.")
finally:
    sock.close()
