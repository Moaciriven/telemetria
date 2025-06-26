import socket
import time
import math
import random

# =============================================
# CONSTANTES FÍSICAS (NUNCA MUDAM)
# =============================================
class PhysicalConstants:
    GRAVITY = 9.80665  # m/s²
    EARTH_RADIUS = 6371000  # metros
    AIR_DENSITY_SEA = 1.225  # kg/m³
    DEG_TO_RAD = math.pi / 180.0
    RAD_TO_DEG = 180.0 / math.pi


# =============================================
# PARÂMETROS DO FOGUETE
# =============================================
class RocketParameters:
    def __init__(self):
        self.MASS = 0.5             # kg
        self.CROSS_AREA = 0.005     # m²
        self.DRAG_COEF = 0.4
        self.thrust_force = 0       # N (será configurado)
        self.burn_time = 0          # s (será configurado)
        self.launch_angle = 0       # graus (será configurado)

    def set_thrust(self, new_thrust):
        self.thrust_force = new_thrust

    def set_burn_time(self, new_time):
        self.burn_time = new_time

    def set_launch_angle(self, new_angle):
        self.launch_angle = new_angle


# =============================================
# PARÂMETROS DA MISSÃO
# =============================================
class MissionParameters:
    def __init__(self):
        self.launch_site = {
            'lat': -24.046746, 
            'lon': -52.378203,
            'alt': 0.0
        }
        self.heading = 0
        self.wind_x = 0.0
        self.wind_y = 0.0

    def set_launch_site(self, lat, lon, alt=0.0):
        self.launch_site = {'lat': lat, 'lon': lon, 'alt': alt}

    def set_heading(self, new_heading):
        self.heading = new_heading

    def set_wind(self, wind_x, wind_y):
        max_wind = 100  # m/s
        self.wind_x = max(min(wind_x, max_wind), -max_wind)
        self.wind_y = max(min(wind_y, max_wind), -max_wind)


# =============================================
# MOTOR FÍSICO
# =============================================
class PhysicsEngine:
    def __init__(self, rocket_params, mission_params):
        self.rocket = rocket_params
        self.mission = mission_params
        self.const = PhysicalConstants()
        self.reset_state()

    def reset_state(self):
        self.state = {
            'time': 0.0,
            'x': 0.0,
            'y': 0.0,
            'altitude': 0.0,
            'vx': 0.0,
            'vy': 0.0,
            'vz': 0.0,
            'acceleration': 0.0
        }

    def calculate_drag(self, velocity, altitude):
        air_density = self.const.AIR_DENSITY_SEA * math.exp(-altitude / 8000)
        return 0.5 * air_density * self.rocket.DRAG_COEF * self.rocket.CROSS_AREA * velocity**2

    def update_position(self):
        angle_rad = self.rocket.launch_angle * self.const.DEG_TO_RAD
        heading_rad = self.mission.heading * self.const.DEG_TO_RAD

        thrust = self.rocket.thrust_force if self.state['time'] < self.rocket.burn_time else 0
        thrust_x = thrust * math.cos(angle_rad) * math.cos(heading_rad)
        thrust_y = thrust * math.cos(angle_rad) * math.sin(heading_rad)
        thrust_z = thrust * math.sin(angle_rad)

        velocity_total = math.sqrt(self.state['vx']**2 + self.state['vy']**2 + self.state['vz']**2)
        drag = self.calculate_drag(velocity_total, self.state['altitude'])
        weight = self.rocket.MASS * self.const.GRAVITY

        ax = thrust_x / self.rocket.MASS + self.mission.wind_x
        ay = thrust_y / self.rocket.MASS + self.mission.wind_y
        az = (thrust_z - weight - drag) / self.rocket.MASS if thrust > 0 else -self.const.GRAVITY

        self.state['vx'] += ax * 0.1
        self.state['vy'] += ay * 0.1
        self.state['vz'] += az * 0.1

        self.state['x'] += self.state['vx'] * 0.1
        self.state['y'] += self.state['vy'] * 0.1
        self.state['altitude'] += self.state['vz'] * 0.1

        self.state['acceleration'] = math.sqrt(ax**2 + ay**2 + az**2)
        self.state['time'] += 0.1

        return self.state


# =============================================
# SIMULADOR PRINCIPAL
# =============================================
class RocketSimulator:
    def __init__(
        self,
        thrust=40,
        burn_time=1.5,
        angle=60,
        mass=0.5,
        heading=0,
        wind_x=0.0,
        wind_y=0.0,
        udp_ip="127.0.0.1",
        udp_port=5555
    ):
        self.UDP_IP = udp_ip
        self.UDP_PORT = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.rocket_params = RocketParameters()
        self.rocket_params.set_thrust(thrust)
        self.rocket_params.set_burn_time(burn_time)
        self.rocket_params.set_launch_angle(angle)
        self.rocket_params.MASS = mass

        self.mission_params = MissionParameters()
        self.mission_params.set_heading(heading)
        self.mission_params.set_wind(wind_x, wind_y)

        self.physics_engine = PhysicsEngine(self.rocket_params, self.mission_params)

    def get_gps_position(self, x, y, alt):
        dlat = (y / PhysicalConstants.EARTH_RADIUS) * PhysicalConstants.RAD_TO_DEG
        dlon = (x / (PhysicalConstants.EARTH_RADIUS *
                     math.cos(self.mission_params.launch_site['lat'] * PhysicalConstants.DEG_TO_RAD))) * PhysicalConstants.RAD_TO_DEG

        return {
            'lat': self.mission_params.launch_site['lat'] + dlat,
            'lon': self.mission_params.launch_site['lon'] + dlon,
            'alt': alt
        }

    def get_telemetry_data(self):
        state = self.physics_engine.state
        gps = self.get_gps_position(state['x'], state['y'], state['altitude'])
        return f"{gps['lat']:.6f},{gps['lon']:.6f},{gps['alt']:.2f},{state['acceleration']:.2f}"

    def send_data(self, data):
        self.sock.sendto(data.encode(), (self.UDP_IP, self.UDP_PORT))

    def run_simulation(self):
        print("[SIM] Iniciando simulação de foguete PET")
        print(f"[SIM] Local: {self.mission_params.launch_site}")
        print(f"[SIM] Direção: {self.mission_params.heading}°")
        print(f"[SIM] Empuxo: {self.rocket_params.thrust_force}N por {self.rocket_params.burn_time}s")
        print(f"[SIM] Ângulo: {self.rocket_params.launch_angle}°")

        try:
            last_update = 0
            self.physics_engine.reset_state()

            while self.physics_engine.state['altitude'] >= 0:
                self.physics_engine.update_position()

                if self.physics_engine.state['time'] - last_update >= 0.1:
                    telemetry = self.get_telemetry_data()
                    self.send_data(telemetry)
                    last_update = self.physics_engine.state['time']

                    print(f"[SIM] t={self.physics_engine.state['time']:.1f}s | "
                          f"alt={self.physics_engine.state['altitude']:.1f}m | "
                          f"dist={math.sqrt(self.physics_engine.state['x']**2 + self.physics_engine.state['y']**2):.1f}m")

                time.sleep(0.1)

            print("[SIM] Foguete caiu. Fim da simulação.")
            self.send_data("END")

        except KeyboardInterrupt:
            print("\n[SIM] Simulação interrompida")
        finally:
            self.sock.close()


# =============================================
# EXECUÇÃO
# =============================================
if __name__ == "__main__":
    rocket = RocketSimulator(
        thrust=80,        # Empuxo em N
        burn_time=1.5,    # Tempo de queima
        angle=45,         # Ângulo de lançamento
        mass=0.5,         # Massa do foguete
        heading=90,        # Direção do lançamento
        wind_x=2.0,       # Vento lateral
        wind_y=0.0        # Vento frontal
    )

    rocket.run_simulation()
