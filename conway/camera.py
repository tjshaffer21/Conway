#! /usr/bin/evn python
# -*- coding: utf-8 -*-
# TODO
#  * Zooming past 0.25 stops shrinking rect.
#  * Zooming past 1.0 adds gaps between tiles

"""camera.py: Implement and control a camera for the system."""

class Camera(object):

    """The Camera class is the class used to render a part of the world onto the
    screen. """

    def __init__(self, pos=[0,0], viewport=[100,100], zoom=1.0):
        """Initialize the Camera class.

        Args
          pos - List; The position [x,y] of the camera in screen coordinates.
          viewport - List; The viewport [w,h] of the camera.
          zoom - Float; Percentage of zoom where 1.0 is normal.
        """
        self._pos = pos
        self._viewport = viewport
        self._zoom = zoom

    @property
    def viewport(self):
        """Return the viewport for the camera.

        Return
          list
        """
        return self._viewport

    @property
    def position(self):
        """Return the position for the camera.

        Return
          list
        """
        return self._pos
    
    @property
    def x(self):
        """Return the x position for the camera.

        Return
          int
        """
        return self._pos[0]

    @x.setter
    def x(self, value):
        """Set the new x position for the camera.

        Args
          value - Float
        """
        self._pos[0] = value

    @property
    def y(self):
        """Return the y position for the camera.
        
        Return
          int
        """
        return self._pos[1]

    @y.setter
    def y(self, value):
        """Set the new y position for the camera.

        Args
          value - Float
        """
        self._pos[1] = value

    @property
    def zoom(self):
        """Return the zoom percentage.

        Return
          Float
        """
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        """Set the zoom percentage.

        Args
          value - Float
        """
        self._zoom = value

    def move(self, value):
        """Move the camera to a new location.

        Args
          value - List; The new location of the camera [x,y].
        """
        self._pos = loc

    def resize(self, value):
        """Resize the viewport of the camera.

        Args
          value - List; The new viewport of the camera [w,h].
        """
        self._viewport = value
