#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""camera.py: Implement and control a camera for the system."""

__version__ = "0.1"

class Camera(object):

    """The Camera class is the class used to view a subsection of the
       world/tilemap on screen.

    Public Attributes:
      viewport - List. The viewable portion of the camera.
      position - List. The location of the Top-Left corner of the 
                 camera.
             x - Int. The x value (Top) of the position.
             y - Int. The y value (Left) of the position.
          zoom - Float. The magnified view percentage between 0.0 and 1.0.
    """

    def __init__(self, pos=[0,0], viewport=[100,100], zoom=1.0, offset=[0,0]):
        """Initialize the Camera class.

        Parameters
               pos - List; The position [x,y] of the camera in screen
                     coordinates.
          viewport - List; The viewport [w,h] of the camera.
              zoom - Float; Percentage of zoom where 1.0 is normal.
            offset - List. An offset amout for where the camera actually starts
                     being rendered.
        """
        self.__pos = pos
        self.__viewport = viewport
        self.__zoom = zoom
        self.__offset = offset

    @property
    def offset(self):
        """Return the offset for the camera.
       
        Return
          list
        """
        return self.__offset

    @offset.setter
    def offset(self, value):
        """Set the offset for the camera.

        Parameters
          value - List
        """
        self.__offset = value

    @property
    def viewport(self):
        """Return the viewport for the camera.

        Return
          list
        """
        return self.__viewport

    @property
    def position(self):
        """Return the position for the camera.

        Return
          list
        """
        return self.__pos
    
    @property
    def x(self):
        """Return the x position for the camera.

        Return
          int
        """
        return self.__pos[0]

    @x.setter
    def x(self, value):
        """Set the new x position for the camera.

        Parameters
          value - Float
        """
        self.__pos[0] = value

    @property
    def y(self):
        """Return the y position for the camera.
        
        Return
          int
        """
        return self.__pos[1]

    @y.setter
    def y(self, value):
        """Set the new y position for the camera.

        Parameters
          value - Float
        """
        self.__pos[1] = value

    @property
    def zoom(self):
        """Return the zoom percentage.

        Return
          float
        """
        return self.__zoom

    @zoom.setter
    def zoom(self, value):
        """Set the zoom percentage.

        Parameters
          value - Float
        """
        if value >= 0 and value <= 1.0:
            self.__zoom = value

    def move(self, value):
        """Move the camera to a new location.

        Parameters
          value - List; The new location of the camera [x,y].
        """
        self.__pos = value

    def resize(self, value):
        """Resize the viewport of the camera.

        Parameters
          value - List; The new viewport of the camera [w,h].
        """
        self.__viewport = value
