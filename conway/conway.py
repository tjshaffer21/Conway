# -*- coding: utf-8 -*-
"""conway.py: Implementation of Conway's Game of Life."""

import sys, random
import pygame

RED = pygame.Color(150,0,0,0)

class State(object):
    """Class to hold the state of the environment.

    Attributes:
        living (int): The number of living cells.
    Args:
        width        (int): The width for the conway data.
        height       (int): The height for the conway data.
        tile_size   (list): The tile size for the TileMap
    """

    def __init__(self, width, height):
        self._width = width
        self._height = height

        self._conway = seed(self._width, self._height)
        self._generations = 1
        self.living = 0

        for i in self._conway:
            self.living += i.count(1)

    @property
    def width(self):
        """Get the width of the conway system.

        Returns:
          int
        """
        return self._width

    @property
    def height(self):
        """Get the height of the conway system.

        Returns:
          int
        """
        return self._height

    @property
    def conway(self):
        """Get the conway data

        Returns:
          list
        """
        return self._conway

    @property
    def generations(self):
        """Get the number of generations that have passed.

        Returns:
          int
        """
        return self._generations

    def add_generation(self):
        """Add a generation to the generation counter."""
        self._generations += 1


def colorize(conway, color_grid):
    """Sets colors for the conway system.

    Post:
        Arg *color_grid* is modified.

    Args:
        conway      (list): List holding conway environment
        color_grid  (list): List holding color environment.
    """
    for x in range(0, len(conway)):
        for y in range(0, len(conway[x])):
            current = color_grid.get_current_chunk()[x][y]
            if conway[x][y] == 0:
                if current.color != pygame.Color('black'):
                    current.color =pygame.Color('black')
            else:
                if current.color == pygame.Color('black'):
                    # Red is set to 150 so that the living cell does not blend
                    # into the background much.
                    current.color = RED
                else:
                    color = current.color
                    if color.r < 255:
                        ncolor = pygame.Color(color.r+1, color.g, color.b, color.a)
                        current.color = ncolor
                    elif color.g < 255:
                        ncolor = pygame.Color(color.r, color.g+1, color.b, color.a)
                        current.color = ncolor
                    elif color.b < 255:
                        ncolor = pygame.Color(color.r, color.g, color.b+1, color.a)
                        current.color = ncolor

def conway_iteration(conway):
    """One interation for conway.

    An iteration is one full sweep of the environment where all cells are
    changed "simultaneously".

    Post
        Arg *conway* is modified.

    Args
      conway (list): the list that holds the data for conway.
    Returns:
      int: The number of living cells.
    """
    def alive(x,y):
        """Check if a cell is alive.

        Alive is defined as currently living (1) or dying (-1); where dying
        indicates a temporary indicator.

        Args:
          x (int): Row in conway.
          y (int): Col in conway.
        Return
          boolean
        """
        return True if conway[x][y] == -1 or conway[x][y] == 1 else False

    def num_neighbors(x,y):
        """Return the number of neighbors.

        Args:
          x (int): Row in conway
          y (int): Col in conway
        Returns:
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

def seed(width, height):
    """Create the initial environment.

    Parameters
        width  (int): The width of the environment.
        height (int): The height of the environment.
    Returns:
      list
    """
    def get_neighbors(x, y):
        """Get the neighbors of (x,y).

        Args:
            x (int)
            y (int)
        Returns:
            list
        """
        neighbors = []

        if x > 0:
            neighbors.append([x-1,y])

        if x < width-1:
            neighbors.append([x+1,y])

        if y > 0:
            neighbors.append([x,y-1])

        if y < height-1:
            neighbors.append([x,y+1])

        if x > 0 and y > 0:
            neighbors.append([x-1,y-1])

        if x < width-1 and y < height-1:
            neighbors.append([x+1,y+1])

        return neighbors

    seeds = [[random.random() for x in range(width)]
             for y in range(height)]

    # For each cell, get the neighbors.
    # If the neighbor's value is <= 0.5 then remove else
    # if random value is < 0 remove.
    for x in range(0, width):
        for y in range(0, height):
            neighbors = get_neighbors(x,y)

            for i in neighbors:
                if seeds[i[1]][i[0]] < seeds[y][x]:
                    if seeds[i[1]][i[0]] <= 0.5:
                        seeds[i[1]][i[0]] = 0
                    elif random.random() < 0.5:
                        seeds[i[1]][i[0]] = 0

    # Final environment should only be 0 or 1.
    for x in range(0, len(seeds)):
        for y in range(0, len(seeds[x])):
            seeds[x][y] = round(seeds[x][y])

    return seeds