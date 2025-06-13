import socket
import time
import math
import numpy as np
import random

# Configurações UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Parâmetros do foguete
dt = 0.1  # passo de tempo (s)
g = 9.81  # gravidade (m/s²)

print("[SIM] Iniciando simulação de foguete PET...")
print(f"[SIM] Enviando dados para {UDP_IP}:{UDP_PORT} a cada {dt} segundos.")

# Parâmetros fixos para o lançamento
massa = 0.5  # kg
area_transversal = 0.003  # m²
forca_propulsao = 200  # N
tempo_propulsao = 0.3  # s

# Localização inicial
lat0 = -23.550520
lon0 = -46.633308
alt0 = 0.0  # chão

# Estado inicial
t = 0.0
alt = alt0
vel = 0.0

print(f"[SIM] Lançamento! Força: {forca_propulsao:.0f}N, Massa: {massa:.2f}kg")

try:
    while alt >= 0.0:  # enquanto não caiu
        # Fase de propulsão
        if t < tempo_propulsao:
            forca = forca_propulsao
        else:
            forca = 0.0

        # Força resultante (propulsão - gravidade - arrasto)
        densidade_ar = 1.2  # kg/m³
        coef_arrasto = 0.5
        arrasto = 0.5 * densidade_ar * coef_arrasto * area_transversal * vel**2
        forca_resultante = forca - massa * g - arrasto
        
        # Aceleração
        acc = forca_resultante / massa
        
        # Atualiza velocidade e altitude
        vel += acc * dt
        alt += vel * dt
        
        # Gera pequena variação aleatória na posição
        variacao = np.random.normal(0, 0.00001)
        lat = lat0 + variacao
        lon = lon0 + variacao
        
        # Envia dados via UDP
        data = f"{lat:.6f},{lon:.6f},{alt:.2f},{vel:.2f}"
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
        print(f"[SIM] t={t:.1f}s | alt={alt:.1f}m | vel={vel:.1f} m/s")

        t += dt
        time.sleep(dt)
    
    print("[SIM] Foguete caiu. Fim da simulação.")
    # Envia sinal de fim
    sock.sendto(b"END", (UDP_IP, UDP_PORT))
    
except KeyboardInterrupt:
    print("\n[SIM] Interrompido pelo usuário.")
finally:
    sock.close()