import pygame


class Group:
    def __init__(self, group_id, base_pos):
        self.id = group_id
        self.state = "pista"  # Estados posibles: "pista", "yendo_bano", "en_bano",
        # "yendo_bar", "en_bar", "vuelve_pista"
        self.destination = base_pos.copy()  # Destino central del grupo
        self.wait_time = 0
        self.members = []  # Lista de agentes pertenecientes al grupo
        self.leader = None  # Agente líder del grupo

    def add_member(self, agent, is_leader=False, offset=None):
        if offset is None:
            offset = pygame.Vector2(0, 0)
        agent.group_offset = offset
        self.members.append(agent)
        if is_leader:
            self.leader = agent
