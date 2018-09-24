# -*- coding: utf-8 -*-
"""container.py: A module for handling UI containers."""

from collections import Iterable
import pygame
from . import ui_object

class SurfaceContainer(ui_object.UIObject):
    """A container that pairs a group of objects with a specific Surface.

    Attributes:
        surface (pygame.Surface)

    Args:
        rect (pygame.Rect)
        surface (pygame.Surface, Iterable):
            If surface == None then surface is the size of the rect.
            If surface == Iterable then the size is the specified dimension.
            If surface == pygame.Surface then pygame.Surface is the surface.
    Errors:
        TypeError: If surface is not of allowable type.
    """

    def __init__(self, rect, surface=None):
        super().__init__(rect)

        if surface == None:
            if isinstance(rect, pygame.Rect):
                self.surface = pygame.Surface([rect.w, rect.h])
            else:
                self.surface = pygame.Surface([rect[2], rect[3]])
        elif isinstance(surface, Iterable):
            self.surface = pygame.Surface(surface)
        elif isinstance(surface, pygame.Surface):
            self.surface = surface
        else:
            raise TypeError("surface must be type pygame.Surface, Iterable, or None")
        self.objects = []

    def add(self, obj: ui_object.UIObject):
        self.objects.append(obj)