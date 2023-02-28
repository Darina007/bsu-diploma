import math
import random

import neat
import pygame

import configuration
from utils import draw_utils, file_utils, game_utils, vizuai
from objects.Cactus import Cactus
from objects.Dino import Dino

game_speed = configuration.game_speed
score = configuration.score
generation = configuration.generation
score_speedup = configuration.score_speedup
enemies = []
dinosaurs = []


def init_genomes(genomes, nets, skins_copy, names_copy):
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        skin = "default"
        if len(skins_copy):
            skin = skins_copy.pop()

        name = "Дино"
        if len(names_copy):
            name = names_copy.pop()

        dinosaurs.append(Dino(30, configuration.height - 170, skin, name))


def save_statistic(path):
    file_utils.mkdir_if_not_exist(path)
    stats.save_genome_fitness(filename=path + '/fitness_history.csv')
    stats.save_species_count(filename=path + '/speciation.csv')
    stats.save_species_fitness(filename=path + '/species_fitness.csv')


def run_game(genomes, config):
    global game_speed, score, enemies, dinosaurs, generation, score_speedup
    generation += 1
    game_speed = configuration.game_speed * generation
    score = 0
    score_speedup = 100
    enemies = [Cactus(configuration.width + 300 / random.uniform(0.8, 3), configuration.height - 85),
               Cactus(configuration.width * 2 + 200 / random.uniform(0.8, 3), configuration.height - 85),
               Cactus(configuration.width * 3 + 400 / random.uniform(0.8, 3), configuration.height - 85)]
    nets = []
    skins_copy = configuration.skins[:]
    names_copy = configuration.names[:]

    init_genomes(genomes, nets, skins_copy, names_copy)

    pygame.init()
    screen = pygame.display.set_mode((configuration.width, configuration.height))
    clock = pygame.time.Clock()
    road_chunks = [
        [pygame.image.load('sprites/road.png'), [0, configuration.height - 100]],
        [pygame.image.load('sprites/road.png'), [2404, configuration.height - 100]]
    ]
    font = pygame.font.SysFont("Roboto Condensed", 30)
    score_font = pygame.font.SysFont("Roboto Condensed", 40)
    dname_font = pygame.font.SysFont("Roboto Condensed", 30)
    heading_font = pygame.font.SysFont("Roboto Condensed", 70)

    while True:
        while generation >= 10 or score >= 10000:
            save_statistic('statistic')
            screen.fill(configuration.bg)
            vizuai.plot_stats(stats, True, True)
            vizuai.plot_species(stats, False, 'graphics/speciation.png')
            vizuai.draw_net(config, stats.best_genome(), filename='graphics/best_genome', show_disabled=True)
            fitness_img = pygame.image.load('./graphics/avg_fitness.png')
            screen.blit(fitness_img, (0, 0))
            screen.blit(pygame.image.load('./graphics/speciation.png'), (fitness_img.get_width() + 10, 0))
            screen.blit(pygame.image.load('./graphics/best_genome.png'), (0, fitness_img.get_height() + 10))
            pygame.display.update()
            game_utils.end_event()

        game_utils.end_event()

        if len(dinosaurs) == 0:
            break

        screen.fill(configuration.bg)
        draw_utils.proceed_road(screen, road_chunks, game_speed)

        # draw dino
        for dino in dinosaurs:
            dino.update()
            dino.draw(screen, font)

        # generate enemies
        if len(enemies) < 3:
            enemies.append(Cactus(enemies[len(enemies) - 1].hitbox.x + configuration.width / random.uniform(0.8, 3),
                                  configuration.height - 85))

        # draw enemies
        rem_list = []
        for i, enemy in enumerate(enemies):
            enemy.update()
            enemy.draw(screen)

            if not enemy.is_active:
                rem_list.append(i)
                continue

            game_utils.delete_dinosaur(dinosaurs, enemy, genomes, nets)

        game_utils.delete_cactus(dinosaurs, enemies, rem_list, genomes)

        game_utils.update_dino_fitness(nets, dinosaurs, enemies, game_speed, genomes)

        score += 0.5 * (game_speed / 4)
        if score > score_speedup:
            game_utils.increase_game_speed(score_speedup, game_speed)

        draw_utils.display_info_items(screen, score_font, "Score: " + str(math.floor(score)), (50, 50, 50),
                                      (configuration.width - 100, 50))

        for i, dinosaur in enumerate(dinosaurs):
            draw_utils.display_info_items(screen, dname_font, dinosaur.name, (170, 238, 187),
                                          (configuration.width - 100, 100 + (i * 25)))

        draw_utils.display_info_items(screen, heading_font, "Generation: " + str(generation), (0, 72, 186),
                                      (configuration.width / 2, 150))

        draw_utils.display_info_items(screen, score_font, "Speed: " + str(game_speed / 8) + "x", (50, 50, 50),
                                      (150, 50))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(run_game, 1000)
