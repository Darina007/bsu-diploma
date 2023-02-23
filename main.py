import pygame
import random
import sys
import math
import neat
import configuration
from Dino import DinoState
from Dino import Dino
from Cactus import Cactus

game_speed = configuration.game_speed
score = configuration.score
generation = configuration.generation
score_speedup = configuration.score_speedup
enemies = []
dinosaurs = []

def calc_dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def run_game(genomes, config):
    global game_speed, score, enemies, dinosaurs, generation, score_speedup

    generation += 1
    game_speed = 8.0
    score = 0
    score_speedup = 100
    enemies = [Cactus(configuration.width + 300 / random.uniform(0.8, 3), configuration.height - 85),
               Cactus(configuration.width * 2 + 200 / random.uniform(0.8, 3), configuration.height - 85),
               Cactus(configuration.width * 3 + 400 / random.uniform(0.8, 3), configuration.height - 85)]
    dinosaurs = []
    nets = []
    skins_copy = configuration.skins[:]
    names_copy = configuration.names[:]

    # init genomes
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0  # every genome is not successful at the start

        skin = "default"
        if len(skins_copy):
            skin = skins_copy.pop()

        name = "Дино"
        if len(names_copy):
            name = names_copy.pop()

        dinosaurs.append(Dino(30, configuration.height - 170, skin, name))

    # init
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

    # dinosaurs = [Dino(30, height-170, "subaru", "Howdy")]

    # the loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display bg & road
        screen.fill(configuration.bg)
        for road_chunk in road_chunks:
            if road_chunk[1][0] <= -2400:
                road_chunk[1][0] = road_chunks[len(road_chunks) - 1][1][0] + 2400

                road_chunks[0], road_chunks[1] = road_chunks[1], road_chunks[0]
                break

            road_chunk[1][0] -= game_speed
            screen.blit(road_chunk[0], (road_chunk[1][0], road_chunk[1][1]))

        # draw dino
        for dino in dinosaurs:
            dino.update()
            dino.draw(screen, font)

        # quit if there is no dinos left
        if len(dinosaurs) == 0:
            break

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

            for j, dinosaur in enumerate(dinosaurs):
                if dinosaur.hitbox.colliderect(enemy.hitbox):
                    genomes[j][1].fitness -= 10  # lower fitness (failed)
                    dinosaurs.pop(j)

                    genomes.pop(j)
                    nets.pop(j)

        for i in rem_list:
            enemies.pop(i)

            for j, dinosaur in enumerate(dinosaurs):
                genomes[j][1].fitness += 5  # raise fitness (+5 for every enemy)


        # controls
        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate((dinosaur.hitbox.y,
                                       calc_dist((dinosaur.hitbox.x, dinosaur.hitbox.y), enemies[0].hitbox.midtop),
                                       enemies[0].hitbox.width,
                                       game_speed))

            if output[0] > 0.5 and dinosaur.state is not DinoState.JUMP:
                dinosaur.jump()
                genomes[i][1].fitness -= 1  # every jump lowers the fitness (assuming it's false jump)

        # read user input (jump test)
        # user_input = pygame.key.get_pressed()
        # if user_input[pygame.K_SPACE]:
        #     for dino in dinosaurs:
        #         if not dino.state == DinoState.JUMP:
        #             dino.jump()

        # score & game speed
        score += 0.5 * (game_speed / 4)
        if score > score_speedup:
            score_speedup += 100 * (game_speed / 2)
            game_speed += 1
            print(f"Game speed increased - {game_speed}")

        score_label = score_font.render("Очки: " + str(math.floor(score)), True, (50, 50, 50))
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (configuration.width - 100, 50)
        screen.blit(score_label, score_label_rect)

        # display dinosaurs names
        for i, dinosaur in enumerate(dinosaurs):
            dname_label = dname_font.render(dinosaur.name, True, (170, 238, 187))
            dname_label_rect = dname_label.get_rect()
            dname_label_rect.center = (configuration.width - 100, 100 + (i * 25))
            screen.blit(dname_label, dname_label_rect)

        # display generation
        label = heading_font.render("Поколение: " + str(generation), True, (0, 72, 186))
        label_rect = label.get_rect()
        label_rect.center = (configuration.width / 2, 150)
        screen.blit(label, label_rect)

        # display game speed
        score_label = score_font.render("Скорость: " + str(game_speed / 8) + "x", True, (50, 50, 50))
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (150, 50)
        screen.blit(score_label, score_label_rect)

        # flip & tick
        pygame.display.flip()
        clock.tick(60)  # fixed 60 fps


if __name__ == "__main__":
    # setup config
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # init NEAT
    p = neat.Population(config)

    # run NEAT
    p.run(run_game, 1000)
