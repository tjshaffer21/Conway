#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""conway.py: Implementation of Conway's Game of Life."""

__version__ = "0.1"

import pygame, sys, random
import tilemap, camera

# TODO - This information can be handled in a better fashion.
SCREEN_SIZE = (800, 600)
GRID_WIDTH = 25
GRID_HEIGHT = 25

# TODO - Delete camera movement; not necessary for final version.
# TODO - Improve seed algorithm.
# TODO - Keep track of conway generations.
# TODO - Overlay the generation count.
# TODO - Halt loop when total extinction occurs.
# TODO - 4 vertical repeats in similar fashion as 3 vertical.
def main():
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
    pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Conway')

    # Setup Conway
    # Remove this if a more sophisticated seed isn't created.
    def seed_conway(width, height):
        """Create the environemtn and seed it."""
        return [[round(random.random()) for x in range(width)]
                 for y in range(height)]

    def colorize(grid, color_grid):
        """Set the color-grid to random colors based on grid values.

        Args
          grid - 2D list of 0 or 1.
          color_grid - 2D list of Tiles.
        Return
          Modified color_grid.
        """
        for x in range(0, len(grid)):
            for y in range(0, len(grid[x])):
                if grid[x][y] == 0:
                    color_grid[x][y].color = [0,0,0]
                else:
                    color_grid[x][y].color = [int(random.random() * 100),
                                              int(random.random() * 100),
                                              int(random.random() * 100)]
        return color_grid
    
    cam = camera.Camera([0, 0], SCREEN_SIZE)
    grid = tilemap.TileMap(GRID_WIDTH, GRID_HEIGHT, 1)
    conway = seed_conway(GRID_WIDTH, GRID_HEIGHT)
    chunk = colorize(conway, grid.get_current_chunk())

    running = True
    loop = False
    last_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)
            elif pygame.key.get_pressed()[pygame.K_LEFT] != 0:
                cam.x = cam.x + 10
            elif pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
                cam.x = cam.x - 10
            elif pygame.key.get_pressed()[pygame.K_UP] != 0:
                cam.y = cam.y + 10
            elif pygame.key.get_pressed()[pygame.K_DOWN] != 0:
                cam.y = cam.y - 10
            elif pygame.key.get_pressed()[pygame.K_a] != 0:
                cam.zoom = cam.zoom + 0.25
            elif pygame.key.get_pressed()[pygame.K_s] != 0:
                cam.zoom = cam.zoom - 0.25
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                colorize(conway_iteration(conway), chunk)
            elif pygame.key.get_pressed()[pygame.K_SPACE] != 0:
                if loop == False:
                    loop = True
                    pygame.time.set_timer(pygame.USEREVENT+1, 1000)
                else:
                    loop = False
                    pygame.time.set_time(pygame.USEREVENT+1, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.USEREVENT+1:
                if loop == True:
                    colorize(conway_iteration(conway), chunk)

        screen.fill([0, 0, 0]) # Clear Screen

        grid.render(screen, cam)
        pygame.display.update()

    pygame.quit()
    sys.exit()

def conway_iteration(conway):
    """One interation for conway.

    An iteration is one full sweep of the environment where all cells are
    changed "simultaneously".

    The passed list is modified by the function.

    Args
      conway - List; the list that holds the data for conway.
    Return
      List
    """
    def alive(x,y):
        """Check if a cell is alive.

        Alive is defined as currently living (1) or dying (-1); where dying
        indicates a temporary indicator.

        Args
          x - Int; Row in conway.
          y - Int; Col in conway.
        Return
          boolean
        """
        return True if conway[x][y] == -1 or conway[x][y] == 1 else False

    def num_neighbors(x,y):
        """Return the number of neighbors.
        
        Args:
          x - Int; Row in conway
          y - Int; Col in conway
        Return
          int
        """
        value = 0

        if x > 0:
            if alive(x-1, y):
                value = value + 1

        if x < len(conway)-1:
            if alive(x+1, y):
                value = value + 1

        if y > 0:
            if alive(x, y-1):
                value = value + 1

        if y < len(conway[x])-1:
            if alive(x, y+1):
                value = value + 1

        if x > 0 and y > 0:
            if alive(x-1, y-1):
                value = value + 1

        if x < len(conway)-1 and y > 0:
            if alive(x+1, y-1):
                value = value + 1

        if x < len(conway)-1 and y < len(conway[x])-1:
            if alive(x+1, y+1):
                value = value + 1

        if x > 0 and y < len(conway[x])-1:
            if alive(x-1, y+1):
                value = value + 1                    
                    
        return value

    for x in range(0, len(conway)):
        for y in range(0, len(conway[x])):
            if alive(x,y) and \
               (num_neighbors(x,y) <= 1 or num_neighbors(x,y) > 3):
                conway[x][y] = -1
            elif not alive(x,y) and num_neighbors(x,y) == 3:
                conway[x][y] = 2

    for x in range(0, len(conway)):
        for y in range(0, len(conway[x])):
            if conway[x][y] == -1:
                conway[x][y] = 0
            elif conway[x][y] == 2:
                conway[x][y] = 1

    return conway
            

if __name__ == "__main__":
    main()
