#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tile.py

TODO:
    * Handle textures
    * Tile should derivie DirtySprite
"""

from collections import Iterable
import pygame

class Tile(pygame.sprite.Sprite):
    """

    See:
        https://www.pygame.org/docs/ref/sprite.html

    Attributes:
        image (pygame.Surface)
        rect  (pygame.Rect)
    Private Attributes:
        _color (pygame.Color)
    Args:
        size (list): The size of the tile.
        color (pygame.Color, Iterable): Color to fill the tile.
        texture_id   (int):
    Errors:
        TypeError: if color is not pygame.Color or Iterable
    """

    def __init__(self, size, color=pygame.Color(255, 255, 255, 0), texture_id=0):
        super().__init__()
        self.redraw = True

        self.image = pygame.Surface(size)
        self.image.fill(color)

        if isinstance(color, pygame.Color):
            self._color = color
        elif isinstance(color, Iterable):
            self._color = pygame.Color(color[0], color[1], color[2], color[3])
        else:
            raise TypeError("color must be pygame.Color or Iterable")

        self.rect = self.image.get_rect()

    @property
    def color(self):
        """Return the color of the tile.

        Returns:
            pygame.Color
        """
        return self._color

    @color.setter
    def color(self, color):
        """Set the image to a new color.

        Post:
            image is modified.
            color is modified.
            redraw is modified.

        Args:
            color (pygame.Color, list)
        Errors:
            TypeError: if color is not pygame.Color or Iterable
        """
        self.image.fill(color)

        if isinstance(color, pygame.Color):
            self._color = color
        elif isinstance(color, Iterable):
            self._color = pygame.Color(color[0], color[1], color[2], color[3])
        else:
            raise TypeError("color must be pygame.Color or Iterable")

        self.redraw = True
