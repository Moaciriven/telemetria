import sys
import csv
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

class RealTimePlot(QMainWindow):
    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path
        self.setWindowTitle("Telemetria Foguete PET - Tempo Real")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Gráfico de Altitude
        self.plot_alt = pg.PlotWidget(title="Altitude (m)")
        self.plot_alt.setLabel('left', 'Altitude', 'm')
        self.plot_alt.showGrid(x=True, y=True)
        layout.addWidget(self.plot_alt)
        self.curve_alt = self.plot_alt.plot(pen='g')

        # Gráfico de Velocidade
        self.plot_vel = pg.PlotWidget(title="Velocidade (m/s)")
        self.plot_vel.setLabel('left', 'Velocidade', 'm/s')
        self.plot_vel.showGrid(x=True, y=True)
        layout.addWidget(self.plot_vel)
        self.curve_vel = self.plot_vel.plot(pen='b')

        # Dados
        self.timestamps = []
        self.alts = []
        self.vels = []

        # Configura o timer para atualizar o gráfico
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(500)  # Atualiza a cada 500ms

    def update_plot(self):
        if not os.path.exists(self.csv_path):
            return

        try:
            with open(self.csv_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Pula cabeçalho
                alts = []
                vels = []
                for i, row in enumerate(reader):
                    if len(row) < 4:
                        continue
                    try:
                        alts.append(float(row[2]))
                        vels.append(float(row[3]))
                    except ValueError:
                        continue
                
                # Atualiza apenas se houver novos dados
                if len(alts) > len(self.alts):
                    self.alts = alts
                    self.vels = vels
                    self.timestamps = list(range(len(self.alts)))
                    
                    # Atualiza os gráficos
                    self.curve_alt.setData(self.timestamps, self.alts)
                    self.curve_vel.setData(self.timestamps, self.vels)

        except Exception as e:
            print(f"Erro ao ler CSV: {e}")

if __name__ == "__main__":
    # Caminho para o arquivo CSV
    dir_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(dir_path, "..", "data", "dados.csv")

    app = QApplication(sys.argv)
    window = RealTimePlot(csv_path)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())