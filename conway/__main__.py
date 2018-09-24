#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse
import pygame
import system_manager, camera, conway
from tiles import tilemap
from ui import container, label

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

def conway_update(state, tilemap):
    """Update the conway state.

    Post:
        state is modified
        tilemap is modified.

    Args:
        state (conway.State): The conway state
    Returns:
        conway.State
    """
    state.living = conway.conway_iteration(state.conway)
    conway.colorize(state.conway, tilemap)
    state.add_generation()

    return (state, tilemap)

# Handle commandline options.
parser = argparse.ArgumentParser(description='Run Conway\'s Game of Life.')
parser.add_argument('-w', help='Window Size [width,height]')
parser.add_argument('-c', help='Conway Size [width,height]')

args = parser.parse_args()
window = args.w.split(',')
cw = args.c.split(',')

cw[0] = int(cw[0])
cw[1] = int(cw[1])
window[0] = int(window[0])
window[1] = int(window[1])

tile_size = 32 # Adjust tile size. Only one var needed since tiles are square.

# TODO Remove and replace with movement (camera) system.
# Scaling drops FPS to ~30.
# Scale tiles so they fit the entire Surface.
width = cw[0] * tile_size
height = cw[1] * tile_size
if width < window[0] or height < window[1]:
    # Tiles are going to be square so only one check for limit.
    while (width < window[0] and height < window[1]) and tile_size < 64:
        tile_size = tile_size * 2

        width = cw[0] * tile_size
        height = cw[1] * tile_size
elif width > window[0] or height > window[1]:
    # Tiles are going to be square so only one check for limit.
    while (width > window[0] and height > window[1]) and tile_size > 4:
        tile_size = tile_size / 4

        width = cw[0] * tile_size
        height = cw[1] * tile_size

# Setup and configure Pygame.
sm = system_manager.SystemManager([window[0], window[1]], pygame.RESIZABLE, "Conway")
sm.add_font("freesansbold", pygame.font.Font('freesansbold.ttf', 18))
font = sm.get_font("freesansbold")

conway_offset = 20
yw_offset = window[1] - conway_offset
camera = camera.Camera([0, 0], [window[0], yw_offset])

# Setup and configure Conway state.
cw_state = conway.State(cw[0], cw[1])
tm = tilemap.TileMap(cw[0], cw[1], 1, [int(tile_size), int(tile_size)], pygame.Color(150,0,0,0))
conway.colorize(cw_state.conway, tm)

# Create UI
ui_container = container.SurfaceContainer([0, 0, window[0], conway_offset])
cw_container = container.SurfaceContainer([0, conway_offset, window[0], yw_offset])

ui_container.add(label.Label("Generations: ", [0,0, 16, 16], font, WHITE, BLACK))
ui_container.add(label.Label("Living: ", [300, 0, 16, 16], font, WHITE, BLACK))
ui_container.add(label.Label("FPS: ", [600, 0, 16, 16], font, WHITE, BLACK))

gen_label = label.Label(str(cw_state.generations), [125, 0, 16, 16], font,
                        WHITE, BLACK)
liv_label = label.Label(str(cw_state.living), [400, 0, 16, 16], font,
                        WHITE, BLACK)
fps_label = label.Label(str(sm.clock.get_fps()), [650, 0, 16, 16], font,
                        WHITE, BLACK)

ui_container.add(gen_label)
ui_container.add(liv_label)
ui_container.add(fps_label)

sm.add_ui_objects(ui_container, cw_container)

loop = False
while sm.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sm.running = False
        elif event.type == pygame.VIDEORESIZE:
            sm.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            camera.resize([event.w, event.h])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sm.running = False
            elif event.key == pygame.K_RETURN:
                if not loop:
                    conway_update(cw_state, tm)
            elif event.key == pygame.K_SPACE:
                if not loop:
                    loop = True
                    pygame.time.set_timer(pygame.USEREVENT+1, 1000)
                else:
                    loop = False
                    pygame.time.set_timer(pygame.USEREVENT+1, 0)
                conway_update(cw_state, tm)
        elif event.type == pygame.USEREVENT+1:
            if loop:
                conway_update(cw_state, tm)

    if cw_state.living == 0:
        loop = False

    gen_label.text = str(cw_state.generations)
    liv_label.text = str(cw_state.living)
    fps_label.text = str(sm.clock.get_fps())

    # Current, version of Tilemap handles rendering. Therefore, render must
    # be performed before main render which handles the bliting.
    tm.render(cw_container.surface, camera)

    sm.render()
    sm.clock.tick(sm.fps)

sm.quit()
sys.exit()
