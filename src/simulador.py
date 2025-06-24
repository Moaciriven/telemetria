import socket
import time
import math
import random
import numpy as np

class RocketSimulator:
    def __init__(self):
        # Configurações de rede
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5555
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Parâmetros físicos
        self.g = 9.80665  # Gravidade padrão (m/s²)
        self.dt = 0.1     # Passo de simulação (s)
        self.update_interval = 1.0  # Intervalo de envio (s)
        
        # Parâmetros do foguete
        self.mass = 0.3          # kg
        self.cross_area = 0.003  # m²
        self.thrust_force = 200   # N
        self.burn_time = 0.3      # s
        
        # Localização inicial (Paraná - Campo Mourão) Av. Cap. Índio Bandeira, 501 - Vila Carolo, Campo Mourão - PR, 87301-899
        self.origin = {
            'lat': -24.046746, 
            'lon': -52.378203,
            'alt': 0.0  # Altitude pode ser ajustada se necessário
        }

        
        # Estado do foguete
        self.state = {
            'time': 0.0,
            'altitude': 0.0,
            'velocity': 0.0,
            'acceleration': 0.0,
            'position_x': 0.0,
            'position_y': 0.0,
            'velocity_x': 0.0,
            'velocity_y': 0.0
        }
        
        # Fatores ambientais
        self.wind = {
            'x': random.uniform(-0.5, 0.5),
            'y': random.uniform(-0.5, 0.5)
        }
        
        self.last_update = 0.0

    def calculate_drag(self, velocity):
        """Calcula a força de arrasto aerodinâmico"""
        air_density = 1.225 * math.exp(-self.state['altitude']/8000)
        drag_coef = 0.5
        return 0.5 * air_density * drag_coef * self.cross_area * velocity**2

    def update_physics(self):
        """Atualiza o estado físico do foguete"""
        # Força de propulsão (só durante a queima)
        thrust = self.thrust_force if self.state['time'] < self.burn_time else 0
        
        # Forças atuantes
        drag = self.calculate_drag(self.state['velocity'])
        weight = self.mass * self.g
        
        # Aceleração vertical (eixo Z)
        net_force = thrust - weight - drag
        acceleration_z = net_force / self.mass
        
        # Aceleração horizontal (ventos aleatórios - eixos X e Y)
        accel_x = random.gauss(0, 0.1) + self.wind['x']
        accel_y = random.gauss(0, 0.1) + self.wind['y']
        
        # Atualiza estados
        self.state['velocity'] += acceleration_z * self.dt
        self.state['altitude'] += self.state['velocity'] * self.dt
        
        self.state['velocity_x'] += accel_x * self.dt
        self.state['velocity_y'] += accel_y * self.dt
        
        self.state['position_x'] += self.state['velocity_x'] * self.dt
        self.state['position_y'] += self.state['velocity_y'] * self.dt
        
        self.state['acceleration'] = math.sqrt(accel_x**2 + accel_y**2 + acceleration_z**2)
        self.state['time'] += self.dt

    def get_gps_position(self):
        """Converte posição local para coordenadas GPS"""
        earth_radius = 6371000  # Raio da Terra em metros
        
        # Conversão para graus decimais
        dlat = (self.state['position_y'] / earth_radius) * (180 / math.pi)
        dlon = (self.state['position_x'] / (earth_radius * math.cos(math.radians(self.origin['lat'])))) * (180 / math.pi)
        
        return {
            'lat': self.origin['lat'] + dlat,
            'lon': self.origin['lon'] + dlon,
            'alt': self.state['altitude']
        }

    def send_telemetry(self):
        """Envia dados via UDP no formato especificado"""
        gps = self.get_gps_position()
        data = f"{gps['lat']:.6f},{gps['lon']:.6f},{gps['alt']:.2f},{self.state['acceleration']:.2f}"
        self.sock.sendto(data.encode(), (self.UDP_IP, self.UDP_PORT))
        
        # Debug (opcional)
        print(f"[SIM] t={self.state['time']:.1f}s | alt={gps['alt']:.1f}m | accel={self.state['acceleration']:.2f}m/s²")

    def run_simulation(self):
        """Executa o loop principal de simulação"""
        print("[SIM] Iniciando simulação de foguete PET")
        print(f"[SIM] Destino: {self.UDP_IP}:{self.UDP_PORT}")
        print(f"[SIM] Propulsão: {self.thrust_force}N por {self.burn_time}s")
        
        try:
            while self.state['altitude'] >= 0:
                self.update_physics()
                
                # Envia dados no intervalo especificado
                if self.state['time'] - self.last_update >= self.update_interval:
                    self.send_telemetry()
                    self.last_update = self.state['time']
                
                time.sleep(self.dt)
            
            # Final da simulação
            print("[SIM] Foguete caiu. Fim da simulação.")
            self.sock.sendto(b"END", (self.UDP_IP, self.UDP_PORT))
            
        except KeyboardInterrupt:
            print("\n[SIM] Simulação interrompida pelo usuário")
        finally:
            self.sock.close()

if __name__ == "__main__":
    rocket = RocketSimulator()
    rocket.run_simulation()