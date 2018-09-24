# -*- coding: utf-8 -*=
"""label.py: A rect containing text for rndering purposes."""

from collections import Iterable
import pygame
from . import ui_object

class Label(ui_object.UIObject):
    """A Label is a simple rect that can render text.

    Attributes:
        antialias (int): Used to indicate if using antialiasing or not.
    Private Attributes:
        _font (pygame.Font): Font object
        _foreground (pygame.Color,list): Color the text will be rendered.
        _old_text_size (list): The size of the previous text used to clear the
                               surface.
        _text (str): Text to be rendered.
        _redraw (bool): Flag to trigger redrawing.

    Args:
        text (string): Text to be rendered.
        rect (pygame.Rect): Where the label will be rendered in relation to the
                            surface object. The [w,h] components of the Rect will
                            be ignored.
        font (pygame.font.Font)
        foreground (pygame.Color, list): The text color.
    """

    def __init__(self, text: str, rect, font: pygame.font.Font, foreground, background):
        super().__init__(rect)

        self.antialias = 1
        self._background = background
        self._font = font
        self._foreground = foreground
        self._old_text_size = [0,0]
        self._redraw = True
        self._text = text

    def draw(self, surface):
        """Render the label onto the surface.

        Post
            surface is modified.
            _redraw is set to False if originally True.

        Args
            surface (pygame.Surface)
        """
        if self._redraw == True:
            surface.fill(self._background, [self.rect[0], self.rect[1],
                                            self._old_text_size[0], self._old_text_size[1]])
            text = self._font.render(self._text, self.antialias, self._foreground)
            surface.blit(text, self.rect)

            self._redraw = False

    @property
    def background(self) -> pygame.Color:
        """Return the background of the label.

        Returns:
            pygame.Color
        """
        return self._background

    @property
    def foreground(self) -> pygame.Color:
        """Return the foreground of the label.

        Returns:
            pygame.Color
        """
        return self._foreground

    @property
    def text(self) -> str:
        """Return the text of the label.

        Returns:
            str
        """
        return self._text

    @background.setter
    def background(self, background):
        """Change the background color.

        Post:
            _background is modified.
            _redraw is modified.

        Args:
            background (pygame.Color, Iterable)
        Errors:
            TypeError: if not pygame.Color or collections.Iterable
        """
        if isinstance(background, Iterable):
            self._background = pygame.Color(background)
            self._redraw = True
        elif isinstance(background, pygame.Color):
            self._background = background
            self._redraw = True
        else:
            raise TypeError("must be pygame.Color or Iterable")

    @foreground.setter
    def foreground(self, foreground):
        """Change the foreground color.

        Post:
            _foreground is modified.
            _redraw is modified.

        Args:
            foreground (pygame.Color, Iterable)
        Errors:
            TypeError: if not pygame.Color or collections.Iterable
        """
        if isinstance(foreground, Iterable):
            self._foreground = pygame.Color(foreground)
            self._redraw = True
        elif isinstance(foreground, pygame.Color):
            self._foreground = foreground
            self._redraw = True
        else:
            raise TypeError("must be pygame.Color or Iterable")

    @text.setter
    def text(self, text: str):
        """Change the text of the label.

        Post:
            _old_text_size is modified.
            _text is modified.
            _redraw is modified.

        Args:
            text (str): New text string.
        """
        self._old_text_size = self._font.size(self._text)
        self._text = text
        self._redraw = True
