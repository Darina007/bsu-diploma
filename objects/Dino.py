import pygame
from enum import Enum
import configuration

class DinoState(Enum):
    RUN = 1
    JUMP = 2

class Dino:
    name = "Carl"
    jump_power = 10
    cur_jump_power = jump_power
    color = "default"
    sprites = {
        "run": [],
        "jump": []
    }
    image = None
    run_animation_index = [0, 5]
    hitbox = None
    state = DinoState.RUN

    def __init__(self, x, y, color="default", name=None):
        self.color = color
        self.load_sprites()
        self.hitbox = pygame.Rect(x, y, self.sprites["run"][0].get_width(), self.sprites["run"][0].get_height())
        self.image = self.sprites["run"][0]

        if name is not None:
            self.name = name

    def load_sprites(self):
        self.sprites["jump"].append(pygame.image.load(f"sprites/dino/{self.color}_jump.png"))
        self.sprites["run"].append(pygame.image.load(f"sprites/dino/{self.color}_run1.png"))
        self.sprites["run"].append(pygame.image.load(f"sprites/dino/{self.color}_run2.png"))

    def update(self):
        if self.state == DinoState.RUN:
            self.run()
        elif self.state == DinoState.JUMP:
            self.jump()

    def run(self):
        self.sprites["run"][0] = pygame.image.load(f"sprites/dino/{self.color}_run1.png")
        self.sprites["run"][1] = pygame.image.load(f"sprites/dino/{self.color}_run2.png")

        self.image = self.sprites["run"][self.run_animation_index[0] // self.run_animation_index[1]]

        self.run_animation_index[0] += 1
        if self.run_animation_index[0] >= self.run_animation_index[1] * 2:
            self.run_animation_index[0] = 0

    def jump(self):
        if self.state == DinoState.JUMP:
            self.hitbox.y -= self.cur_jump_power * (2 * (configuration.game_speed / 8))
            self.cur_jump_power -= 0.5 * (configuration.game_speed / 8)

            # if self.cur_jump_power <= -self.jump_power:
            #    self.hitbox.y -= self.cur_jump_power * (2 * (game_speed / 8))
            #    self.state = DinoState.RUN
            #    self.cur_jump_power = self.jump_power
            if self.hitbox.y >= configuration.height - 170:
                self.hitbox.y = configuration.height - 170
                self.state = DinoState.RUN
                self.cur_jump_power = self.jump_power
        else:
            self.state = DinoState.JUMP
            self.image = pygame.image.load(f"sprites/dino/{self.color}_jump.png")

    def draw(self, scr, fnt=None):
        scr.blit(self.image, (self.hitbox.x, self.hitbox.y))

        if fnt is not None:
            c_label = fnt.render(self.name.capitalize(), True, (100, 100, 100))
            c_label_rect = c_label.get_rect()
            c_label_rect.center = (self.hitbox.x + 45, self.hitbox.y - 30)
            scr.blit(c_label, c_label_rect)
