# hardtime_csv.py
# Visualizador de dados em tempo real lendo direto do CSV

import sys
import csv
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton
)
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

csv_path = Path("data/dados.csv")
csv_path.parent.mkdir(parents=True, exist_ok=True)

# Dados em memória
timestamps = []
alts = []
vels = []
dados_mem = []

# Interface Qt
app = QApplication([])
window = QWidget()
window.setWindowTitle("Gráfico Tempo Real (CSV)")
layout = QVBoxLayout(window)

plot = pg.GraphicsLayoutWidget()
layout.addWidget(plot)

p1 = plot.addPlot(title="Altitude (m)")
p1.showGrid(x=True, y=True)
curve1 = p1.plot()

p2 = plot.addPlot(title="Velocidade (km/h)", row=1, col=0)
p2.showGrid(x=True, y=True)
curve2 = p2.plot()

btn = QPushButton("Salvar CSV Pós-Análise")
layout.addWidget(btn)

def salvar():
    out = Path("data/dados_visualizacao_salvo.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lat","lon","alt","vel"])
        writer.writerows(dados_mem)
    print(f"[ST] Dados salvos em {out}")

btn.clicked.connect(salvar)

ultima_linha_lida = 0

def update():
    global ultima_linha_lida
    if not csv_path.exists():
        return

    try:
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            if not reader:
                return

            if reader[0] == ["lat", "lon", "alt", "vel"]:
                reader = reader[1:]  # Ignora cabeçalho

            novas_linhas = reader[ultima_linha_lida:]
            for linha in novas_linhas:
                try:
                    lat, lon, alt, vel = map(float, linha)
                    dados_mem.append([lat, lon, alt, vel])
                    timestamps.append(len(timestamps))
                    alts.append(alt)
                    vels.append(vel)
                except ValueError:
                    continue

            ultima_linha_lida += len(novas_linhas)
            curve1.setData(timestamps, alts)
            curve2.setData(timestamps, vels)
    except Exception as e:
        print(f"[ERR] Falha ao ler CSV: {e}")

# Timer para atualização dos gráficos
timer = QTimer()
timer.timeout.connect(update)
timer.start(500)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
