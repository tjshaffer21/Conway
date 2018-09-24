# -*- coding: utf-8 -*-
"""system_manager.py: Module used to configure and handle the pygame subsystem."""

__version__ = '0.1.0'

from collections import Iterable
import pygame
from ui import container

class SystemManager(object):
    """SystemManager manages the various pygame components.

    See:
        https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode

    Attributes:
        clock (pygame.time.Clock): Main system clock.
        fps (int): Framerate. Default=60
        screen:
        running (bool): Flag indicating if the system is running.
    Private Attributes:
        _fonts (dict): Fonts that have been added to the system.
        _root (container.SurfaceContainer):

    Args:
        screen_size (Iterable): The size of the window.
        screen_opt (int): Flags for the screen.
        caption (str): The title of the window.
    """

    def __init__(self, screen_size: Iterable, screen_opt: int, caption: str):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.screen = pygame.display.set_mode(screen_size, screen_opt)

        pygame.display.set_caption(caption)

        self._fonts = {}
        self._root = container.SurfaceContainer([0,0,screen_size[0], screen_size[1]])

    def add_font(self, font_name: str, font: pygame.font.Font):
        """Add a font to the system.

        Post:
            _fonts is modified.

        Args:
            font_name (str): Font identifer
            font      (pygame.font.Font): Font
        """
        self._fonts[font_name] = font

    def add_ui_objects(self, *obj):
        """Add UIObjects into the system's root container.

        Post
            _root is modified.

        Args:
            *obj (UIObject): Unknown number of UIObjects.
        """
        for i in obj:
            self._root.add(i)

    def get_font(self, font_name: str) -> pygame.font.Font:
        """Return the font with given identifier.

        Args:
            font_name (str): Font identifier
        Returns:
            pygame.font.Font
        """
        return self._fonts[font_name]

    def quit(self):
        """Handle clean up and shutdown operations.

        Post:
            pygame system is shut down. Dependent functions will throw errors.
        """
        pygame.quit()

    def render(self):
        """Handle the rendering of the system.

        Post:
            screen is modified.
            _root objects may be modified.
        """
        for i in self._root.objects:
            if isinstance(i, container.SurfaceContainer):
                for j in i.objects:
                    j.draw(i.surface)
                self.screen.blit(i.surface, (i.rect.x, i.rect.y))

        pygame.display.update()
