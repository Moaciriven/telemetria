# analyze.py
# Analisa estatísticas básicas a partir do CSV

import csv
from statistics import mean
from pathlib import Path

csv_path = Path("data/dados.csv")
if not csv_path.exists():
    print(f"[ANL] Arquivo não encontrado: {csv_path}")
    exit(1)

lats = []
lons = []
alts = []
vels = []

with csv_path.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            lats.append(float(row["lat"]))
            lons.append(float(row["lon"]))
            alts.append(float(row["alt"]))
            vels.append(float(row["vel"]))
        except ValueError:
            continue

total = len(alts)
print(f"[ANL] Total de registros válidos: {total}")
if total == 0:
    print("[ANL] Nenhum dado para analisar.")
    exit(0)

def stats(name, data):
    print(f"[ANL] {name} → Min: {min(data):.2f}, Max: {max(data):.2f}, Média: {mean(data):.2f}")

stats("Altitude (m)", alts)
stats("Velocidade (km/h)", vels)
stats("Latitude", lats)
stats("Longitude", lons)
