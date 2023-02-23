import random
import pygame
import configuration

class Cactus:
    available_types = ["1", "2", "3", "4", "5", "6"]
    cactus_type = None
    image = None
    hitbox = None
    is_active = True

    def __init__(self, x, y, forced_type=None):
        if forced_type is not None:
            self.cactus_type = forced_type

        self.load_image()
        self.hitbox.x = x
        self.hitbox.y = y - self.hitbox.height  # origin from bottom

    def randomize_cactus(self):
        self.cactus_type = random.choice(self.available_types)

    def load_image(self):
        if self.cactus_type is None:
            self.randomize_cactus()

        self.image = pygame.image.load(f"sprites/cactus/{self.cactus_type}.png")
        self.hitbox = self.image.get_rect()

    def update(self):
        self.hitbox.x -= configuration.game_speed
        if self.hitbox.x < -self.hitbox.width:
            # remove this cactus
            self.is_active = False

    def draw(self, scr):
        scr.blit(self.image, self.hitbox)
