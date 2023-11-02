from random import randint, randrange, uniform
from typing import Final, List, Tuple

import pygame

ColourType = Tuple[int, int, int]

# Define some colors
BLACK: Final[ColourType] = (0, 0, 0)
WHITE: Final[ColourType] = (255, 255, 255)

SCREEN_WIDTH: Final[int] = 960
SCREEN_HEIGHT: Final[int] = 540
IMG_MAX_SIZE: Final[float] = 100
SCREEN_DIMENSIONS: Final[Tuple[int, int]] = (SCREEN_WIDTH, SCREEN_HEIGHT)

INITIAL_TILE_MOVEMENT_SPEED: Final[float] = 2
RANDOM_SPEED_DELTA: Final[float] = 0.1
RANDOM_SIZE_DELTA: Final[float] = 2
STARTING_NUMBER_OF_SPRITES: Final[int] = 1
CONFETTI_PARTICLE_SIZE: Final[int] = 5
CONFETTI_PARTICLE_SPEED: Final[int] = 5
NUM_OF_PARTICLES_TO_SPAWN_PER_TICK: Final[int] = 100


def randsign(n: float) -> float:
    if randint(0, 1) == 0:
        return -n
    return n


def rand_colour() -> ColourType:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)


class Particle:
    def __init__(self, starting_pos: Tuple[float, float], vector: pygame.math.Vector2) -> None:
        self.pos: Tuple[float, float] = starting_pos
        self.vector = vector
        self.colour = rand_colour()

    def update_pos(self) -> None:
        self.pos = (
            self.pos[0] + uniform(self.vector.x, self.vector.x*2),
            self.pos[1] + uniform(self.vector.y, self.vector.y*2),
        )


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_DIMENSIONS)

    pygame.display.set_caption("Particles")

    done = False
    clock = pygame.time.Clock()
    speed_multiplier: float = 1
    pygame.key.set_repeat(600, 60)

    confetti_particles: List[Particle] = []

    while not done:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    done = True
                case pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        particle_vector = pygame.math.Vector2(
                            CONFETTI_PARTICLE_SPEED * speed_multiplier,
                            CONFETTI_PARTICLE_SPEED * speed_multiplier,
                        )
                        mouse_pos = pygame.mouse.get_pos()
                        for _ in range(NUM_OF_PARTICLES_TO_SPAWN_PER_TICK):
                            confetti_particles.append(
                                Particle(
                                    mouse_pos,
                                    particle_vector.rotate(randrange(360)),
                                ),
                            )
                case _:
                    pass

        screen.fill(WHITE)

        for particle in confetti_particles:
            particle.update_pos()
            offscreen_buffer = 100 # stop instant despawn
            particle_is_on_screen = (
                particle.pos[0] <= (SCREEN_DIMENSIONS[0] + offscreen_buffer)
                and particle.pos[1] <= (SCREEN_DIMENSIONS[1] + offscreen_buffer)
                and particle.pos[0] >= -offscreen_buffer
                and particle.pos[1] >= -offscreen_buffer
            )
            if not particle_is_on_screen:
                confetti_particles.remove(particle)
            else:
                pygame.draw.rect(
                    screen,
                    particle.colour,
                    (
                        particle.pos[0],
                        particle.pos[1],
                        CONFETTI_PARTICLE_SIZE,
                        CONFETTI_PARTICLE_SIZE,
                    ),
                )

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
