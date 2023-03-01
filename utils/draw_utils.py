def display_cactus(enemy, screen):
    enemy.update()
    enemy.draw(screen)


def display_dinos(dinosaurs, screen, font):
    for dino in dinosaurs:
        dino.update()
        dino.draw(screen, font)


def display_info_items(screen, item_font, text, coords, center_coords):
    item_label = item_font.render(text, True, coords)
    item_label_rect = item_label.get_rect()
    item_label_rect.center = center_coords
    screen.blit(item_label, item_label_rect)


def proceed_road(screen, road_chunks, game_speed):
    for road_chunk in road_chunks:
        if road_chunk[1][0] <= -2400:
            road_chunk[1][0] = road_chunks[len(road_chunks) - 1][1][0] + 2400

            road_chunks[0], road_chunks[1] = road_chunks[1], road_chunks[0]
            break

        road_chunk[1][0] -= game_speed
        screen.blit(road_chunk[0], (road_chunk[1][0], road_chunk[1][1]))
