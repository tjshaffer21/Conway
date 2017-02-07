#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""conway.py: Implementation of Conway's Game of Life."""

__version__ = "0.2"

import pygame, sys, random
import tilemap, camera

class State(object):

    """Class to hold the state of the environment.
    
    Public Attributes
            width - Int. The width of the conway system.
           height - Int. The height of the conway system.
           conway - List. The conway system.
      generations - Int. Number of generations that have passed.
          tilemap - TileMap. The TileMap used for renderng.
           camera - Camera. The Camera used in conjunction with the TileMap.
    """

    def __init__(self, conway_width, conway_height, tile_size=[32,32]):
        """Initialize the State.

        Parameters
           conway_width - Int; the width for the conway data.
          conway_height - Int; the height for the conway data.
              tile_size - List; the tile size for the TileMap
        """
        self.__width = conway_width
        self.__height = conway_height
        
        self.__conway = self.seed()
        self.__generations = 1
        self.__living = 0
        
        for i in self.__conway:
            self.__living += i.count(1)
        
        self.__world = tilemap.TileMap(self.__width, self.__height, 1,
                                       tile_size)
        self.__camera = camera.Camera([0,0],
                                      [pygame.display.get_surface().get_width(),
                                       pygame.display.get_surface().get_height()])

        for x in range(0, self.__width):
            for y in range(0, self.__height):
                if self.__conway[y][x] == 0:
                    self.__world.get_current_chunk()[y][x].color = [0,0,0]
                else:
                    self.__world.get_current_chunk()[y][x].color = [150,0,0]

    @property
    def width(self):
        """Get the width of the conway system.

        Return
          int
        """
        return self.__width

    @property
    def height(self):
        """Get the height of the conway system.

        Return
          int
        """
        return self.__height

    @property
    def conway(self):
        """Get the conway data

        Return
          list
        """
        return self.__conway

    @property
    def generations(self):
        """Get the number of generations that have passed.

        Return
          int
        """
        return self.__generations

    @property
    def living(self):
        """Get the number of living cells.

        Return
          int
        """
        return self.__living

    @living.setter
    def living(self, value):
        """Set the number of living cells.

        Parameters
          value - Int.
        """
        self.__living = value

    @property
    def tilemap(self):
        """Get the tilemap for the system.

        Return
          TileMap
        """
        return self.__world

    @property
    def camera(self):
        """Get the camera for the system.
        
        Return
          Camera
        """
        return self.__camera

    def seed(self):
        """Create the initial environment."""
        return [[round(random.random()) for x in range(self.__width)]
                for y in range(self.__height)]

    def add_generation(self):
        """Add a generation to the generation counter."""
        self.__generations += 1

    
def main(screen_size=[800,600], tile_size=[32,32], conway_size=[25,25]):
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    font = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Conway')

    state = State(conway_size[0], conway_size[1], tile_size)

    def update():
        """Update the conway system."""
        state.living = conway_iteration(state.conway)
        colorize(state.conway, state.tilemap)
        state.add_generation()

    running = True
    loop = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if not loop: # Disable when auto is active
                        update()
                elif event.key == pygame.K_SPACE:
                    if not loop:
                        loop = True
                        pygame.time.set_timer(pygame.USEREVENT+1, 1000)
                    else:
                        loop = False
                        pygame.time.set_timer(pygame.USEREVENT+1, 0)
                    update()
            elif event.type == pygame.USEREVENT+1:
                if loop:
                    update()

        if state.living == 0:
            loop = False

        # Rendering
        screen.fill([0, 0, 0])
        state.tilemap.render(screen, state.camera)

        gen_text = "Generations: " + str(state.generations)
        screen.blit(font.render(gen_text, 1, [255, 255, 255]), [0,0])

        screen.blit(font.render("Living: " + str(state.living), 1,
                                [255, 255, 255]), [len(gen_text) * 20, 0])
        
        pygame.display.update()

    pygame.quit()
    sys.exit()

def conway_iteration(conway):
    """One interation for conway.

    An iteration is one full sweep of the environment where all cells are
    changed "simultaneously".

    Parameers
      conway - List; the list that holds the data for conway.
    Modified Arguments
      conway
    Return
      Int - The number of living cells.
    """
    def alive(x,y):
        """Check if a cell is alive.

        Alive is defined as currently living (1) or dying (-1); where dying
        indicates a temporary indicator.

        Parameters
          x - Int; Row in conway.
          y - Int; Col in conway.
        Return
          boolean
        """
        return True if conway[x][y] == -1 or conway[x][y] == 1 else False

    def num_neighbors(x,y):
        """Return the number of neighbors.
        
        Parameters
          x - Int; Row in conway
          y - Int; Col in conway
        Return
          int
        """
        value = 0

        if x > 0:
            if alive(x-1, y):
                value += 1

        if x < len(conway)-1:
            if alive(x+1, y):
                value += 1

        if y > 0:
            if alive(x, y-1):
                value += 1

        if y < len(conway[x])-1:
            if alive(x, y+1):
                value += 1

        if x > 0 and y > 0:
            if alive(x-1, y-1):
                value += 1

        if x < len(conway)-1 and y > 0:
            if alive(x+1, y-1):
                value += 1

        if x < len(conway)-1 and y < len(conway[x])-1:
            if alive(x+1, y+1):
                value += 1

        if x > 0 and y < len(conway[x])-1:
            if alive(x-1, y+1):
                value += 1                    
                    
        return value

    for x in range(0, len(conway)):
        for y in range(0, len(conway[x])):
            if alive(x,y) and \
               (num_neighbors(x,y) <= 1 or num_neighbors(x,y) > 3):
                conway[x][y] = -1
            elif not alive(x,y) and num_neighbors(x,y) == 3:
                conway[x][y] = 2

    # Check for number of living cells while flipping the cells to their proper
    # states.
    living = 0
    for x in range(0, len(conway)):
        for y in range(0, len(conway[x])):
            if conway[x][y] == -1:
                conway[x][y] = 0
            elif conway[x][y] == 2:
                conway[x][y] = 1
                living += 1
            elif conway[x][y] == 1:
                living += 1

    return living
            
def colorize(conway, color_grid):
    """Sets colors for the conway system.

    Parameters
          conway - List holding conway environment
      color_grid - List holding color environment.
    Modified Arugments
      color_grid
    """
    for x in range(0, len(conway)):
        for y in range(0, len(conway[x])):
            current = color_grid.get_current_chunk
            if conway[x][y] == 0:
                current()[x][y].color = [0,0,0]
            else:
                if current()[x][y].color == [0,0,0]:
                    # Red is set to 150 so that the living cell does not blend
                    # into the background much.
                    current()[x][y].color = [150, 0, 0]
                else:
                    if current()[x][y].color[0] < 255:
                        current()[x][y].color[0] += 1
                    elif current()[x][y].color[1] < 255:
                        current()[x][y].color[1] += 1
                    elif current()[x][y].color[2] < 255:
                        current()[x][y].color[2] += 1

                    
if __name__ == "__main__":
    main([800,600],[10,10],[80,60])
