# -*- coding: utf-8 -*-
"""Module used to handle UIObjects."""

from collections import Iterable
import pygame

class UIObject(object):
    """Base object used for all UI objects.

    Attributes:
        rect (pygame.Rect): Rect specifying the location, size of the object.
    Args:
        rect (pygame.Rect, Iterable)
    Errors:
        TypeError: If rect is not a valid type.
    """

    def __init__(self, rect):
        if isinstance(rect, pygame.Rect):
            self.rect = rect
        elif isinstance(rect, Iterable):
            self.rect = pygame.Rect(rect)
        else:
            raise TypeError("rect must be a pygame.Rect or collections.Iterable")
