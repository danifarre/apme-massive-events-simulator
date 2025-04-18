import random

import pygame

from common.constants import PROB_SEPARATION, SEPARATION_TIME_MIN, SEPARATION_TIME_MAX, AGENT_SPEED, WAIT_TIME_MIN, \
    WAIT_TIME_MAX, PROB_GROUP_MOVE
from simulation.simulation import SimulationZone
from common.utils import random_point_in_rect


class Agent:
    id = 0

    def __init__(self, pos, group, is_leader=False, group_offset=pygame.Vector2(0, 0)):
        Agent.id += 1
        self.id = Agent.id

        self.pos = pygame.Vector2(pos)
        self.radius = 2
        self.color = (0, 0, 255)  # Azul
        self.speed = AGENT_SPEED
        self.group = group  # Referencia a la instancia de Group a la que pertenece
        self.is_leader = is_leader
        self.group_offset = group_offset  # Pequeño offset respecto al destino central del grupo
        # Atributos para separación temporal
        self.separated = False
        self.separation_time = 0
        self.own_destination = None

    @property
    def state(self):
        return self.group.state

    @state.setter
    def state(self, new_state):
        self.group.state = new_state

    @property
    def destination(self):
        return self.group.destination

    @destination.setter
    def destination(self, new_dest):
        self.group.destination = new_dest

    @property
    def wait_time(self):
        return self.group.wait_time

    @wait_time.setter
    def wait_time(self, new_wait):
        self.group.wait_time = new_wait

    def update(self):
        if self.is_leader:
            self.update_leader()
        else:
            self.update_follower()
        self.move_towards_destination()

    def update_leader(self):
        # Si el grupo está esperando en baño o bar
        if self.state in ["en_bano", "en_bar"]:
            self.wait_time -= 1
            if self.wait_time <= 0:
                self.state = "vuelve_pista"
                # El destino al volver se elige dentro de la pista
                self.destination = random_point_in_rect(SimulationZone.zone_crowd)
            return

        # Si el grupo está en la pista, el líder decide mover al grupo
        if self.state == "pista":
            if random.random() < PROB_GROUP_MOVE:
                if random.random() < 0.5:
                    self.state = "yendo_bano"
                    self.destination = random_point_in_rect(random.choice(SimulationZone.zone_bathrooms))
                else:
                    self.state = "yendo_bar"
                    self.destination = random_point_in_rect(random.choice(SimulationZone.zone_bars))
        # Si el grupo se dirige a baño o bar
        if self.state in ["yendo_bano", "yendo_bar"]:
            if (self.pos - self.destination).length() < self.speed:
                self.state = "en_bano" if self.state == "yendo_bano" else "en_bar"
                self.wait_time = random.randint(WAIT_TIME_MIN, WAIT_TIME_MAX)
        # Si el grupo vuelve a la pista
        if self.state == "vuelve_pista":
            if (self.pos - self.destination).length() < self.speed:
                self.state = "pista"
                self.destination = random_point_in_rect(SimulationZone.zone_crowd)

    def update_follower(self):
        # Si ya está separado, actualiza la separación temporal
        if self.separated:
            if (self.own_destination - self.pos).length() < self.speed or self.separation_time <= 0:
                self.separated = False
                self.own_destination = None
            else:
                self.separation_time -= 1
            return
        # Con cierta probabilidad se separa temporalmente
        if random.random() < PROB_SEPARATION:
            self.separated = True
            self.separation_time = random.randint(SEPARATION_TIME_MIN, SEPARATION_TIME_MAX)
            self.own_destination = random_point_in_rect(SimulationZone.zone_crowd)
            return

    def move_towards_destination(self):
        # Si está separado, se mueve hacia su destino individual; si no, hacia (destino del grupo + offset)
        target = self.own_destination if self.separated else (self.destination + self.group_offset)
        direction = target - self.pos
        if direction.length() > self.speed:
            self.pos += direction.normalize() * self.speed
        else:
            self.pos = target

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
