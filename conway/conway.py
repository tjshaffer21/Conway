# -*- coding: utf-8 -*-
"""conway.py: Implementation of Conway's Game of Life.

Attributes:
    living_cell (pygame.Color): The initial color of a cell when it becomes alive.
    dead_cell (pygame.Color): The color of a non-living cell.
"""

import sys, random
import pygame

living_cell = pygame.Color(150, 0, 0, 0)
dead_cell = pygame.Color(0, 0, 0, 0)

class State(object):
    """Class to hold the state of the environment.

    Attributes:
        conway (list): 2D list containing the current state of the conway en-
                       vironment.
        living (int): The number of living cells.
    Args:
        width  (int): The width for the conway data.
        height (int): The height for the conway data.
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._generations = 1
        self.living = 0
        self.conway = _seed(self._width, self._height)

        for i in self.conway:
            self.living += i.count(1)

    @property
    def width(self) -> int:
        """Return the width of the system.

        Returns:
          int
        """
        return self._width

    @property
    def height(self) -> int:
        """Return the height of the system.

        Returns:
          int
        """
        return self._height

    @property
    def generations(self) -> int:
        """Return the number of generations that have passed.

        Returns:
          int
        """
        return self._generations

    def inc_generation(self):
        """Increment the generation counter.

        Post:
            _generations is modified.
        """
        self._generations += 1


def colorize(conway: list, color_grid: list) -> list:
    """Sets colors for the conway system.

    Pre:
        color_grid must be the list as defined in tiles.tilemap.
    Post:
        Arg color_grid is modified.

    Args:
        conway (list): conway list
        color_grid (list): color list.
    Returns:
        list: color_grid is returned
    """
    for y in range(0, len(conway)):
        for x in range(0, len(conway[y])):
            current = color_grid.get_current_chunk()[y][x]
            if conway[y][x] == 0:
                if current.color != dead_cell:
                    current.color = dead_cell
            else:
                if current.color == dead_cell:
                    current.color = living_cell
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

    return color_grid

def increment(conway: list) -> int:
    """Increment conway by one.

    Post
        Arg conway is modified.

    Args:
      conway (list): conway list
    Returns:
      int: The number of living cells.
    """
    def alive(arr: list, xy: tuple) -> bool:
        """Check if a cell is alive.

        Alive is defined as currently living (1) or dying (-1); where dying
        indicates a temporary indicator.

        Args:
            arr (list): conway list
            xy (tuple): Position in arr defined in (x,y)
        Returns:
          boolean
        """
        return True if arr[xy[1]][xy[0]] == -1 or arr[xy[1]][xy[0]] == 1 else False

    def num_neighbors(arr: list, xy: tuple) -> int:
        """Return the number of living neighbors.

        Args:
            arr (list): conway list
            xy (tuple): Position in arr using (x,y) values.
        Returns:
          int
        """
        value = 0

        for i in _moore_neighbors(arr, xy):
            if alive(conway, i):
                value += 1

        return value

    for y in range(0, len(conway)):
        for x in range(0, len(conway[y])):
            if alive(conway, (x, y)) and \
               (num_neighbors(conway, (x, y)) <= 1 or num_neighbors(conway, (x, y)) > 3):
                conway[y][x] = -1
            elif not alive(conway, (x, y)) and num_neighbors(conway, (x, y)) == 3:
                conway[y][x] = 2

    # Check for number of living cells while flipping the cells to their proper
    # states.
    living = 0
    for y in range(0, len(conway)):
        for x in range(0, len(conway[y])):
            if conway[y][x] == -1:
                conway[y][x] = 0
            elif conway[y][x] == 2:
                conway[y][x] = 1
                living += 1
            elif conway[y][x] == 1:
                living += 1

    return living

def update(state: State, color_grid: list) -> tuple:
    """Update the conway state.

    Pre:
        color_grid must be the list as defined in tiles.tilemap.
    Post:
        state is modified
        color_grid is modified.

    Args:
        state (conway.State): The conway state
    Returns:
        tuple (conway.State, list): State and color_grid are returned.
    """
    state.living = increment(state.conway)
    colorize(state.conway, color_grid)
    state.inc_generation()

    return (state, color_grid)

def _moore_neighbors(arr: list, xy: tuple) -> tuple:
    """Obtain a list of Moore's neighbours.

    Pre:
        arr must be a 2D list.

    Args:
        arr (list): 2d list.
        xy  (tuple): (x,y) values coresponding to the x,y values in arr.
    Returns:
        list: A list of tuples holding the neighbor's (x,y) values.
     """
    width = len(arr[0])-1
    height = len(arr)-1
    neighbors = []

    for x in range(xy[0]-1, xy[0]+2):
        for y in range(xy[1]-1, xy[1]+2):
            if (x >= 0 and y >= 0) and (x <= width and y <= height):
                if not (xy[0] == x and xy[1] == y):
                    neighbors.append((x, y))

    return neighbors

def _seed(width: int, height: int) -> list:
    """Create the initial environment.

    Args:
        width  (int): The width of the environment.
        height (int): The height of the environment.
    Returns:
      list
    """
    seeds = [[random.random() for _ in range(width)] for _ in range(height)]

    # For each cell, get the neighbors.
    # If the neighbor's value is <= 0.5 then remove else
    # if random value is < 0 remove.
    for x in range(0, width):
        for y in range(0, height):
            for i in _moore_neighbors(seeds, (x,y)):
                if seeds[i[1]][i[0]] < seeds[y][x]:
                    if seeds[i[1]][i[0]] <= 0.5:
                        seeds[i[1]][i[0]] = 0
                    elif random.random() < 0.5:
                        seeds[i[1]][i[0]] = 0

    # Final environment should only be 0 or 1.
    for y in range(0, height):
        for x in range(0, width):
            seeds[y][x] = round(seeds[y][x])

    return seeds
