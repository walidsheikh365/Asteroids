import pygame
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y, rotation, shot_speed):
        super().__init__(x, y, 5)
        self.rotation = rotation
        self.velocity = pygame.Vector2(0, 1).rotate(rotation) * shot_speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius)
    
    def update(self, dt):
        self.position += self.velocity * dt
