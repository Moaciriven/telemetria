# udp_getter.py
# Captura dados UDP e grava em CSV

import socket
import csv
from pathlib import Path

UDP_PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

csv_path = Path("data/dados.csv")
csv_path.parent.mkdir(parents=True, exist_ok=True)

print(f"[UDP] Aguardando dados na porta {UDP_PORT}...")

try:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lat", "lon", "alt", "vel"])
        while True:
            data, _ = sock.recvfrom(1024)
            lat, lon, alt, vel = data.decode().split(",")
            writer.writerow([lat, lon, alt, vel])
            print(f"[UDP] Salvo: alt={alt}, vel={vel}")
except KeyboardInterrupt:
    print("\n[UDP] Encerrando captura.")
finally:
    sock.close()


