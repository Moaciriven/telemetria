import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Caminho do CSV
dir_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(dir_path, "..", "data", "dados.csv")

if not os.path.exists(csv_path):
    print("Arquivo de dados não encontrado.")
    exit()

df = pd.read_csv(csv_path)

if df.empty:
    print("Nenhum dado para analisar.")
    exit()

# Métricas básicas
alt_max = df['alt'].max()
vel_max = df['vel'].max()
duracao = len(df) * 0.1  # supondo 0.1s por amostra

# Encontra o pico de velocidade
pico_velocidade = df['vel'].idxmax()

# Calcula aceleração
df['acc'] = df['vel'].diff() / 0.1  # derivada da velocidade
acc_max = df['acc'].max()

# Distância percorrida (horizontal)
pos_inicial = (df.iloc[0]['lat'], df.iloc[0]['lon'])
pos_final = (df.iloc[-1]['lat'], df.iloc[-1]['lon'])
distancia = geodesic(pos_inicial, pos_final).meters

print("\n=== Análise do Voo ===")
print(f"Altitude Máxima: {alt_max:.2f} m")
print(f"Velocidade Máxima: {vel_max:.2f} m/s")
print(f"Aceleração Máxima: {acc_max:.2f} m/s²")
print(f"Duração do voo: {duracao:.1f} s")
print(f"Distância horizontal: {distancia:.2f} m")
print(f"Pico de velocidade em t={pico_velocidade*0.1:.1f}s")

# Gera gráficos de análise
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(df.index*0.1, df['alt'], 'g-')
plt.title('Altitude vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Altitude (m)')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(df.index*0.1, df['vel'], 'b-')
plt.title('Velocidade vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(dir_path, "..", "data", "analise_voo.png"))
print("\nGráfico de análise salvo em data/analise_voo.png")