
import constants
import pygame

from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, cooldown_timer=0.0):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 180
        self.cooldown_timer = cooldown_timer
    
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), constants.LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        
        if keys[pygame.K_SPACE]:
            shot = self.shoot()
            
            # if shot:
            #     shot.add(self.containers)
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_SPEED * dt

    def shoot(self):
        if self.cooldown_timer > 0:
            return None
        else:
            self.cooldown_timer = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
            return Shot(self.position.x, self.position.y, self.rotation, constants.PLAYER_SHOT_SPEED)