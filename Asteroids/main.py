import pygame
import sys

from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player







def main():
    pygame.init()
    game_clock = pygame.time.Clock()
    
    asteroids = pygame.sprite.Group()
    asteroidfield = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # asteroid = Asteroid(100, 100, 20)

    dt = 180

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")




    while True:

        
        log_state()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill("black")
        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

            if shots:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        asteroid.split()
                        shot.kill()
                        log_event("asteroid_shot")

        for drawable_sprite in drawable:
            drawable_sprite.draw(screen)

        pygame.display.flip()
        game_clock.tick(60)
        dt = game_clock.get_time() / 1000.0

        # print(f"Frame time: {dt:.4f} seconds, FPS: {game_clock.get_fps():.2f}")


if __name__ == "__main__":
    main()
