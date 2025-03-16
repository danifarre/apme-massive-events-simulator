import random

import pygame


def random_point_in_rect(rect):
    """Devuelve un punto (x, y) aleatorio dentro de un pygame.Rect."""
    x = random.randint(rect.left, rect.right)
    y = random.randint(rect.top, rect.bottom)
    return pygame.Vector2(x, y)


def draw_label_centered(surface, text, rect, font, color=(0, 0, 0)):
    """Dibuja 'text' centrado dentro del rectángulo 'rect'."""
    label = font.render(text, True, color)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)
