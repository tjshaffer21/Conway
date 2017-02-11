#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tilemap.py: Create and manage the tile map for pygame system."""

__version__ = "0.1"

class Tile(object):

    """The Tile class holds information for each tile of a tile map.

    Public Attributes
      color - List. The RGBA values to associate with a Tile.
      texture - Int. An ID key for the texture.
    """
    
    def __init__(self, color = [255,255,255,0], texture_id = 0):
        """Initialize the class.

        Parameters
               color - List. RGBA values for the Tile.
          texture_id - Int. ID key for the texture.
        """
        self.__color = color
        self.__texture = texture_id

    @property
    def color(self):
        """Return list."""
        return self.__color

    @color.setter
    def color(self, value):
        """Set the color to value.
        
        Parameters
          value - List of RGBA values.
        """
        self.__color = value

    @property
    def texture(self):
        """Get the texture ID.
        
        Return
          int
        """
        return self.__texture

    @texture.setter
    def texture(self, value):
        """Set the texture to value.

        Parameters
          value - Integer
        """
        self.__texture = value


class TileMap(object):

    """TileMap is a data structure containing tiles to for a map.

    The TileMap is divided up into a number of chunks each of a given width and
    height, and each tile is of equal size.

    Public Attributes
          tile_size - List. The width and height of a Tile.
         tile_width - Int. The width of a Tile.
        tile_height - Int. The height of a Tile.
         chunk_size - List. The width and hight of a chunk.
        chunk_width - Int. The width of a chunk.
       chunk_height - Int. The height of a chunk.
      current_chunk - Int. The current "active" (centered) chunk. For convience,
                      the chunks are 1-based rather than 0-based.
    """

    def __init__(self, width, height, num_chunks=1, tile_size=[32,32]):
        """Initialize the class.

        Parameters
               width - Integer. The width of a chunk in the tile map.
              height - Integer. The height of a chunk in the tile map.
          num_chunks - Integer. The number of chunks in the tile map.
           tile_size - List of Integers. The size of a Tile in the tile map.
        """
        self.__tile_size = tile_size
        self.__current_chunk = 1
        self.__total_chunks = num_chunks
        self.__chunk_size = [width, height]
        self.__map = [[[Tile() for x in range(width)] for y in range(height)]
                     for z in range(num_chunks)]

    @property
    def tile_size(self):
        """Return the size of the tiles.
        
        Return
          list
        """
        return self.__tile_size

    @property
    def tile_width(self):
        """Return the width of the tiles.

        Return
          int
        """
        return self.__tile_size[0]

    @property
    def tile_height(self):
        """Return the height of the tiles.

        Return
          int
        """
        return self.__tile_size[1]

    @property
    def chunk_size(self):
        """Return the chunk size.

        Return
          list
        """
        return self.__chunk_size

    @property
    def chunk_width(self):
        """Return the chunk's width.

        Return
          int
        """
        return self.__chunk_size[0]

    @property
    def chunk_height(self):
        """Return the chunk's height.

        Return
          int
        """
        return self.__chunk_size[1]

    @property
    def current_chunk(self):
        """Return the current chunk that is being focused on.

        Return
          int
        """
        return self.__current_chunk

    @current_chunk.setter
    def current_chunk(self, value):
        """Change the chunk that is being focused on.

        Chunks are 1-based so value must be [1, __total_chunks].

        Parameters
          value - Integer
        Error
          ValueError
        """
        if value <= 0 or value > self.__total_chunks:
            raise ValueError(str(value) + " outside of chunk range.")
        
        self.__current_chunk = value

    def get_center(self):
        """Return the coordinates of the center point.

        Return
          list
        """
        return [self.__chunk_size[0] / 2, self.__chunk_size[1] / 2]
        
    def get_current_chunk(self):
        """Return the current chunk.
        
        Return
          list
        """
        return self.__map[self.__current_chunk-1]

    def get_chunk(self, chunk):
        """Return the specified chunk.

        Return
          list
        """
        if chunk <= 0 or chunk > self.__total_chunks:
            return None

        return self.__map[chunk-1]

    def render(self, surface, cam):
        """Render the world onto the screen.

        Parameters
          surface - SDL_Surface; The surface to work with.
              cam - Camera; The camera in which everything is rendered.
        Modified Arguments
          surface
        """
        chunk = self.get_current_chunk()
        for x in range(cam.x, cam.viewport[0], self.tile_width):
            #if x < 0 or x > surface.get_width():
            #    continue

            for y in range(cam.y, cam.viewport[1], self.tile_height):
                x_tile = int(x / self.tile_width)
                y_tile = int(y / self.tile_height)

                if x_tile >= 0 and x_tile < self.chunk_width \
                   and y_tile >= 0 and y_tile < self.chunk_height:
                    wc = screen_to_world([x, y], cam.position)
                    tl_x = (wc[0] * cam.zoom) + cam.offset[0]
                    tl_y = (wc[1] * cam.zoom) + cam.offset[1]
                    w = self.tile_width
                    h = self.tile_height

                    if x + self.tile_width > cam.viewport[0]:
                        w = x - cam.viewport[0]
                    if y + self.tile_height > cam.viewport[1]:
                        h = y - cam.viewport[1]
                    if x + self.tile_width >= cam.viewport[0] and \
                       y + self.tile_height >= cam.viewport[1]:
                        w = x - cam.viewport[0]
                        h = y - cam.viewport[1]
                    surface.fill(chunk[y_tile][x_tile].color,
                                 [tl_x, tl_y, w, h])


def screen_to_world(screen_coord, cam_coord):
    """Convert screen coordinates into world coordinates.

    Parameters
      screen_coord - List; screen coordinates to convert.
         cam_coord - List; camera coordinates.
    Return
      list
    """
    return [screen_coord[0] - cam_coord[0], screen_coord[1] - cam_coord[1]]
