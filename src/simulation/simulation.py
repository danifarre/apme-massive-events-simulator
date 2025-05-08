import random
from datetime import datetime, timezone

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

        # Dibujar agentes
        for agent in self.agents:
            agent.draw(self.screen)
        pygame.display.flip()

    def send_info(self, msg_service):
        message = dict()

        for device in self.devices:
            result = msg_service.send_message(device.take_measure(), "devices")
            if result == 1:
                break

        for agent in self.agents:
            message["user_id"] = agent.id
            message["lat"] = agent.pos.x
            message["lon"] = agent.pos.y
            message["height"] = 5.0 if agent.id is not 100 else 1.0
            message["speed"] = 1.0 if agent.id is not 100 else 5.0
            message["timestamp"] = datetime.now(timezone.utc).isoformat()
            result = msg_service.send_message(message, "users-info")
            if result == 1:
                break
