import random
from datetime import datetime, timezone
import threading

import pygame

from common.constants import WIDTH, HEIGHT, NUM_AGENTS, GROUP_SIZE_MIN, GROUP_SIZE_MAX
from agents.group import Group
from devices.anemometer import Anemometer
from devices.infrared_flame_detector import InfraredFlameDetector
from devices.smoke_detector import SmokeDetector
from devices.thermometer import Thermometer
from messages.messaging_service import MessagingService
from simulation.simulation_zone import SimulationZone
from agents.agent import Agent
from common.utils import random_point_in_rect, draw_label_centered


class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simulador de Conciertos")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.agents = []
        self.groups = []
        self.devices = []
        self.next_group_id = 0
        self.create_devices()
        self.create_groups_and_agents(NUM_AGENTS)
        self.running = True
        self.evacuate_zone = False
        self.flame_detector = True
        self.devices_firing = False
        self.fall = False

        threading.Thread(target=self.listen_terminal_input, daemon=True).start()

    def listen_terminal_input(self):
        while True:
            user_input = input("Introduce 1 para evacuar la zona marcada, 0 para volver a permitir el acceso\n"
                               "Introduce 2 para apagar un detector de llama, 3 para volver a encenderlo\n"
                               "Introduce 4 para que se disparen los detectores de humo y llama, 5 para volver a valores normales\n"
                               "Introduce 6 para simular la caída de un asistente, 7 para que se levante\n"
                               "Entrada: ").strip()
            if user_input == "1":
                self.evacuate_zone = True
                print("Activada evacuación de la zona crítica.")
            elif user_input == "0":
                self.evacuate_zone = False
                print("Desactivada evacuación. Los agentes pueden volver a entrar.")
            elif user_input == "2":
                self.flame_detector = False
                print("Desactivada detector de llama.")
            elif user_input == "3":
                self.flame_detector = True
                print("Activada detector de llama.")
            elif user_input == "6":
                self.fall = True
                print("Caída de asistente.")
            elif user_input == "7":
                self.fall = False
                print("El asistente se levanta.")

    def create_groups_and_agents(self, num_agents):
        remaining = num_agents
        while remaining > 0:
            group_size = random.randint(GROUP_SIZE_MIN, GROUP_SIZE_MAX)
            if group_size > remaining:
                group_size = remaining
            base_pos = random_point_in_rect(SimulationZone.zone_crowd)
            # Crear un grupo
            group = Group(self.next_group_id, base_pos)
            self.next_group_id += 1
            self.groups.append(group)
            # Crear agentes para este grupo
            for i in range(group_size):
                if i == 0:
                    offset = pygame.Vector2(0, 0)
                    pos = base_pos.copy()
                    is_leader = True
                else:
                    offset = pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10))
                    pos = base_pos + offset
                    is_leader = False
                agent = Agent(pos, group, is_leader, offset)
                self.agents.append(agent)
                group.add_member(agent, is_leader, offset)
            remaining -= group_size

    def create_devices(self):
        self.devices.append(Thermometer("Termómetro"))
        self.devices.append(Anemometer("Anemómetro"))
        self.devices.append(InfraredFlameDetector("Detector de llama (Baño Izquierda)"))
        self.devices.append(InfraredFlameDetector("Detector de llama (Baño Derecha)"))
        self.devices.append(InfraredFlameDetector("Detector de llama (Bar Izquierda)"))
        self.devices.append(InfraredFlameDetector("Detector de llama (Bar Derecha)"))
        self.devices.append(SmokeDetector("Detector de humo (Baño Izquierda)"))
        self.devices.append(SmokeDetector("Detector de humo (Baño Derecha)"))
        self.devices.append(SmokeDetector("Detector de humo (Bar Izquierda)"))
        self.devices.append(SmokeDetector("Detector de humo (Bar Derecha)"))

    def run(self):
        msg_service = MessagingService()
        message_send_indicator = 0

        while self.running:

            self.clock.tick(30)
            self.handle_events()
            self.update()
            self.draw()
            if message_send_indicator == 30:
                self.send_info(msg_service)
                message_send_indicator = 0
            else:
                message_send_indicator += 1
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        for agent in self.agents:
            agent.update()

        critical_zone = pygame.Rect(
            SimulationZone.zone_crowd.right - 300,  # más ancho
            SimulationZone.zone_crowd.top,  # parte superior
            300,  # ancho ampliado
            180  # alto ampliado
        )

        safe_zone = pygame.Rect(
            SimulationZone.zone_crowd.right - 200,
            SimulationZone.zone_crowd.bottom - 100,
            180,
            80
        )

        if self.evacuate_zone:
            for group in self.groups:
                leader = group.leader
                if leader and critical_zone.collidepoint(leader.pos.x, leader.pos.y):
                    if group.state == "pista":
                        group.state = "vuelve_pista"
                        group.destination = random_point_in_rect(safe_zone)

    def draw(self):
        self.screen.fill((255, 255, 255))  # Fondo blanco

        # Dibujar zonas
        GRAY = (200, 200, 200)
        BLACK = (0, 0, 0)
        pygame.draw.rect(self.screen, GRAY, SimulationZone.zone_stage)
        pygame.draw.rect(self.screen, GRAY, SimulationZone.zone_bathroom_left)
        pygame.draw.rect(self.screen, GRAY, SimulationZone.zone_bathroom_right)
        pygame.draw.rect(self.screen, GRAY, SimulationZone.zone_bar_left)
        pygame.draw.rect(self.screen, GRAY, SimulationZone.zone_bar_right)
        pygame.draw.rect(self.screen, (255, 255, 255), SimulationZone.zone_crowd)

        # Dibujar contornos (líneas separadoras)
        pygame.draw.rect(self.screen, BLACK, SimulationZone.zone_stage, 2)
        pygame.draw.rect(self.screen, BLACK, SimulationZone.zone_bathroom_left, 2)
        pygame.draw.rect(self.screen, BLACK, SimulationZone.zone_bathroom_right, 2)
        pygame.draw.rect(self.screen, BLACK, SimulationZone.zone_bar_left, 2)
        pygame.draw.rect(self.screen, BLACK, SimulationZone.zone_bar_right, 2)
        pygame.draw.rect(self.screen, BLACK, SimulationZone.zone_crowd, 2)

        # Dibujar etiquetas centradas
        draw_label_centered(self.screen, "Escenario", SimulationZone.zone_stage, self.font)
        draw_label_centered(self.screen, "Baños (Izq)", SimulationZone.zone_bathroom_left, self.font)
        draw_label_centered(self.screen, "Baños (Der)", SimulationZone.zone_bathroom_right, self.font)
        draw_label_centered(self.screen, "Bar (Izq)", SimulationZone.zone_bar_left, self.font)
        draw_label_centered(self.screen, "Bar (Der)", SimulationZone.zone_bar_right, self.font)
        draw_label_centered(self.screen, "Pista", SimulationZone.zone_crowd, self.font)

        critical_zone = pygame.Rect(
            SimulationZone.zone_crowd.right - 300,  # más ancho
            SimulationZone.zone_crowd.top,  # parte superior
            300,  # ancho ampliado
            180  # alto ampliado
        )

        pygame.draw.rect(self.screen, (255, 0, 0), critical_zone, 2)

        # Dibujar agentes
        for agent in self.agents:
            agent.draw(self.screen)
        pygame.display.flip()

    def send_info(self, msg_service):
        message = dict()

        for device in self.devices:
            if self.flame_detector is False:
                if device.get_device_name() != "Detector de llama (Bar Izquierda)":
                    result = msg_service.send_message(device.take_measure(), "devices")
                else:
                    result = 0
            elif self.devices_firing is True:
                if "Bar Derecha" in device.get_device_name():
                    result = msg_service.send_message(device.take_measure(1), "devices")
                else:
                    result = msg_service.send_message(device.take_measure(), "devices")
            else:
                result = msg_service.send_message(device.take_measure(), "devices")
            if result == 1:
                break

        for agent in self.agents:
            message["user_id"] = agent.id
            message["lat"] = agent.pos.x
            message["lon"] = agent.pos.y
            message["height"] = 1.0 if self.fall is True and agent.id == 50 else 5.0
            message["speed"] = 5.0 if self.fall is True and agent.id == 50 else 1.0
            message["timestamp"] = datetime.now(timezone.utc).isoformat()
            result = msg_service.send_message(message, "users-info")
            if result == 1:
                break
