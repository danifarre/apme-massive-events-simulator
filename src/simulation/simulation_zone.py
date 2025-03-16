import pygame

from common.constants import STAGE_HEIGHT, WIDTH, SIDE_ZONE_WIDTH, HALF_SIDE_ZONE, SIDE_ZONE_TOTAL_HEIGHT


class SimulationZone:
    zone_stage = pygame.Rect(0, 0, WIDTH, STAGE_HEIGHT)
    zone_bathroom_left = pygame.Rect(0, STAGE_HEIGHT, SIDE_ZONE_WIDTH, HALF_SIDE_ZONE)
    zone_bathroom_right = pygame.Rect(WIDTH - SIDE_ZONE_WIDTH, STAGE_HEIGHT, SIDE_ZONE_WIDTH, HALF_SIDE_ZONE)
    zone_bar_left = pygame.Rect(0, STAGE_HEIGHT + HALF_SIDE_ZONE, SIDE_ZONE_WIDTH, HALF_SIDE_ZONE)
    zone_bar_right = pygame.Rect(WIDTH - SIDE_ZONE_WIDTH, STAGE_HEIGHT + HALF_SIDE_ZONE, SIDE_ZONE_WIDTH,
                                 HALF_SIDE_ZONE)
    zone_crowd = pygame.Rect(SIDE_ZONE_WIDTH, STAGE_HEIGHT, WIDTH - 2 * SIDE_ZONE_WIDTH, SIDE_ZONE_TOTAL_HEIGHT)
    zone_bathrooms = [zone_bathroom_left, zone_bathroom_right]
    zone_bars = [zone_bar_left, zone_bar_right]
