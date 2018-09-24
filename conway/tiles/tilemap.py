# -*- coding: utf-8 -*-
"""Module to handle the TileMap data structure.

Attributes:
    default_tile_color (pygame.Color): Default color for Tile objects. Primarily,
                                       used when instantiating the TileMap object.
"""

import pygame
from . import tile

default_tile_color = pygame.Color(255,255,255,255)

class TileMap(object):
    """TileMap is a data structure containing tiles to for a map.

    The TileMap is divided up into a number of chunks each of a given width and
    height, and each tile is of equal size.

    Args:
        width       (int): The width of a chunk in the tile map.
        height      (int): The height of a chunk in the tile map.
        num_chunks  (int): The number of chunks in the tile map.
        tile_size   (list): The size of a Tile in the tile map.
    """

    def __init__(self, width, height, num_chunks=1, tile_size=[32,32],
                 tile_color: pygame.Color = default_tile_color):
        self._tile_size = tile_size
        self._current_chunk = 1
        self._total_chunks = num_chunks
        self._chunk_size = [width, height]
        self._map = [[[tile.Tile(size=tile_size, color=tile_color)
                        for x in range(width)]
                     for y in range(height)]
                    for z in range(num_chunks)]

    @property
    def tile_size(self):
        """Return the size of the tiles.

        Returns:
          list
        """
        return self._tile_size

    @property
    def tile_width(self):
        """Return the width of the tiles.

        Returns:
          int
        """
        return self._tile_size[0]

    @property
    def tile_height(self):
        """Return the height of the tiles.

        Returns:
          int
        """
        return self._tile_size[1]

    @property
    def chunk_size(self):
        """Return the chunk size.

        Returns:
          list
        """
        return self._chunk_size

    @property
    def chunk_width(self):
        """Return the chunk's width.

        Returns:
          int
        """
        return self._chunk_size[0]

    @property
    def chunk_height(self):
        """Return the chunk's height.

        Returns:
          int
        """
        return self._chunk_size[1]

    @property
    def current_chunk(self):
        """Return the current chunk that is being focused on.

        Returns:
          int
        """
        return self._current_chunk

    @current_chunk.setter
    def current_chunk(self, value):
        """Change the chunk that is being focused on.

        Chunks are 1-based so value must be [1, _total_chunks].

        Args:
          value (int):
        Error:
          ValueError
        """
        if value <= 0 or value > self._total_chunks:
            raise ValueError(str(value) + " outside of chunk range.")

        self._current_chunk = value

    def get_center(self):
        """Return the coordinates of the center point.

        Returns:
          list
        """
        return [self._chunk_size[0] / 2, self._chunk_size[1] / 2]

    def get_current_chunk(self):
        """Return the current chunk.

        Returns:
          list
        """
        return self._map[self._current_chunk-1]

    def get_chunk(self, chunk):
        """Return the specified chunk.

        Returns:
          list
        """
        if chunk <= 0 or chunk > self._total_chunks:
            return None

        return self._map[chunk-1]

    def render(self, surface, cam):
        """Render the world onto the screen.

        Post:
            surface is modified.

        Args:
            surface (SDL_Surface):
            cam          (Camera):
        """
        chunk = self.get_current_chunk()
        for x in range(cam.x, cam.viewport[0], self.tile_width):
            x_tile = int(x / self.tile_width)
            if x_tile >= 0 and x_tile < self.chunk_width:
                for y in range(cam.y, cam.viewport[1], self.tile_height):
                    y_tile = int(y / self.tile_height)

                    if y_tile >= 0 and y_tile < self.chunk_height:
                        if chunk[y_tile][x_tile].redraw == True:
                            wc = screen_to_world([x, y], cam.position)
                            tl_x = (wc[0] * cam.zoom) + cam.offset[0]
                            tl_y = (wc[1] * cam.zoom) + cam.offset[1]

                            surface.blit(chunk[y_tile][x_tile].image, [tl_x, tl_y])
                            chunk[y_tile][x_tile].redraw = False


def screen_to_world(screen_coord, cam_coord):
    """Convert screen coordinates into world coordinates.

    Args:
        screen_coord (list): screen coordinates to convert.
        cam_coord    (list): camera coordinates.
    Returns:
      list
    """
    return [screen_coord[0] - cam_coord[0], screen_coord[1] - cam_coord[1]]
