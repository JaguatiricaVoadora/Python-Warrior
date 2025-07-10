


import pygame

class LifeBar:
    def __init__(self, x, y, width, height, max_health, border_color=(0,0,0), fill_color=(0,255,0), bg_color=(255,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.border_color = border_color
        self.fill_color = fill_color
        self.bg_color = bg_color

    def update(self, new_health):
        self.current_health = max(0, min(self.max_health, new_health))

    def draw(self, surface):
        # Draw background (lost health)
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        # Draw current health
        fill_width = int(self.width * (self.current_health / self.max_health))
        if fill_width > 0:
            pygame.draw.rect(surface, self.fill_color, (self.x, self.y, fill_width, self.height))
        # Draw border
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2)

    def __init__(self, x, y, width, height, max_health, border_color=(0,0,0), fill_color=(0,255,0), bg_color=(255,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.border_color = border_color
        self.fill_color = fill_color
        self.bg_color = bg_color

    def update(self, new_health):
        self.current_health = max(0, min(self.max_health, new_health))

    def draw(self, surface):
        # Draw background (lost health)
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        # Draw current health
        fill_width = int(self.width * (self.current_health / self.max_health))
        if fill_width > 0:
            pygame.draw.rect(surface, self.fill_color, (self.x, self.y, fill_width, self.height))
        # Draw border
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2)
        # Draw background (lost health)
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        # Draw current health
        fill_width = int(self.width * (self.current_health / self.max_health))
        if fill_width > 0:
            pygame.draw.rect(surface, self.fill_color, (self.x, self.y, fill_width, self.height))
        # Draw border
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2)
