import math
import pygame
import sys

from objects.Dino import DinoState

def increase_game_speed(score_speedup, game_speed):
    score_speedup += 100 * (game_speed / 2)
    game_speed += 1
    print(f"Game speed increased - {game_speed}")

def update_dino_fitness(nets, dinosaurs, enemies, game_speed, genomes):
    for i, dinosaur in enumerate(dinosaurs):
        output = nets[i].activate((dinosaur.hitbox.y,
                                   calc_dist((dinosaur.hitbox.x, dinosaur.hitbox.y),
                                             enemies[0].hitbox.midtop),
                                   enemies[0].hitbox.width,
                                   game_speed))
        if DinoState.RUN:
            genomes[i][1].fitness += 1
        if output[0] > 0.5 and dinosaur.state is not DinoState.JUMP:
            dinosaur.jump()
            genomes[i][1].fitness -= 2  # every jump lowers the fitness (assuming it's false jump)


def calc_dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def end_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def delete_dinosaur(dinosaurs, enemy, genomes, nets):
    for j, dinosaur in enumerate(dinosaurs):
        if dinosaur.hitbox.colliderect(enemy.hitbox):
            genomes[j][1].fitness -= 10  # lower fitness (failed)
            dinosaurs.pop(j)
            genomes.pop(j)
            nets.pop(j)


def delete_cactus(dinosaurs, enemies, rem_list, genomes):
    for i in rem_list:
        enemies.pop(i)
        for j, dinosaur in enumerate(dinosaurs):
            genomes[j][1].fitness += 5  # raise fitness (+5 for every enemy)
