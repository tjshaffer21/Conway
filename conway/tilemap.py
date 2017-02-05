#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO
#  * Texture storage and usage
#  * Chunk implementation
#  * Tile scaling
#  * Fix graphical bugs.
#  * Smoother camera movement for TileMap's render function.
#  * TODO comments within TileMap's render function.

"""tilemap.py: Create and manage the tile map for pygame system."""

__version__ = "0.1"

class Tile(object):

    """The Tile class holds information for each tile of a tile map."""
    
    def __init__(self, color = [255,255,255,0], texture_id = 0):
        """Initialize the class.

        Args
          color - List of RGBA values.
          texture_id - Integer
        """
        self._color = color
        self._texture = texture_id

    @property
    def color(self):
        """Return list."""
        return self._color

    @color.setter
    def color(self, value):
        """Set the color to value.
        
        Args
          value - List of RGBA values.
        """
        self._color = value

    @property
    def texture(self):
        "Return int"
        return self._texture

    @texture.setter
    def texture(self, value):
        """Set the texture to value.

        Args
          value - Integer
        """
        self._texture = value


class TileMap(object):

    """TileMap is a data structure containing tiles to for a map.

    The TileMap is divided up into a number of chunks each of a given width and
    height, and each tile is of equal size."""

    def __init__(self, width, height, num_chunks=1, tile_size=[32,32]):
        """Initialize the class.

        Args
          width - Integer. The width of a chunk in the tile map.
          height - Integer. The height of a chunk in the tile map.
          num_chunks - Integer. The number of chunks in the tile map.
          tile_size - List of Integers. The size of a Tile in the tile map.
        """
        self._tile_size = tile_size
        self._current_chunk = 1
        self._total_chunks = num_chunks
        self._chunk_size = [width, height]
        self._map = [[[Tile() for x in range(width)] for y in range(height)]
                     for z in range(num_chunks)]

    @property
    def tile_size(self):
        """Return the size of the tiles.
        
        Return
          List
        """
        return self._tile_size

    @property
    def tile_width(self):
        """Return the width of the tiles.

        Return
          int
        """
        return self._tile_size[0]

    @property
    def tile_height(self):
        """Return the height of the tiles.

        Return
          int
        """
        return self._tile_size[1]

    @property
    def chunk_size(self):
        """Return the chunk size.

        Return
          list
        """
        return self._chunk_size

    @property
    def chunk_width(self):
        """Return the chunk's width.

        Return
          int
        """
        return self._chunk_size[0]

    @property
    def chunk_height(self):
        """Return the chunk's height.

        Return
          int
        """
        return self._chunk_size[1]

    @property
    def current_chunk(self):
        """Return the current chunk that is being focused on.

        Return
          int
        """
        return self._current_chunk

    @current_chunk.setter
    def current_chunk(self, value):
        """Change the chunk that is being focused on.

        Args
          value - Integer
        """
        self._current_chunk = value

    def get_current_chunk(self):
        """Return the current chunk.
        
        Return
          List
        """
        return self._map[self._current_chunk-1]

    def get_chunk(self, chunk):
        """Return the specified chunk.

        Return
          List
        """
        if chunk <= 0 or chunk > self._total_chunks:
            return None

        return self._map[chunk-1]

    def render(self, surface, cam):
        """Render the world onto the screen.

        Args
          surface - SDL_Surface; The surface to work with.
          cam     - Camera; The camera in which everything is rendered.
        """
        # TODO - This can be removed as a function is complexity isn't added later.
        def screen_to_world(coordinates, cam_coordinates):
            return [coordinates[0] - cam_coordinates[0],
                    coordinates[1] - cam_coordinates[1]]

        chunk = self.get_current_chunk()
        for x in range(cam.x, cam.viewport[0], 32):
            # Don't bother to continue if x is not on screen.
            if x < 0 or x > surface.get_width():
                continue

            for y in range(cam.y, cam.viewport[1], 32):
                x_tile = int(x / self.tile_width)
                y_tile = int(y / self.tile_height)

                if x_tile >= 0 and x_tile < self.chunk_width \
                   and y_tile >= 0 and y_tile < self.chunk_height:
                    # TODO - This can be removed for small gain.
                    wc = screen_to_world([x, y], cam.position)
                    surface.fill(chunk[y_tile][x_tile].color,
                                 [wc[0] * cam.zoom, wc[1] * cam.zoom,
                                  self.tile_width, self.tile_height])
