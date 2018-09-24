#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pygame
from conway.tiles import tile

class TestTileMethods(unittest.TestCase):
    def setUp(self):
        self.t1 = tile.Tile([32,32])
        self.t2 = tile.Tile([32,32], pygame.Color(0,0,0,0))
        self.t3 = tile.Tile([32,32], [100, 100, 100, 0])

    def test_tile_attributes(self):
        self.assertEqual(self.t1.color, pygame.Color(255, 255, 255, 0))
        self.assertEqual(self.t2.color, pygame.Color(0,0,0,0))
        self.assertEqual(self.t3.color, pygame.Color(100,100,100,0))

        self.assertEqual(self.t1.rect, pygame.Rect(0,0,32,32))
        self.assertEqual(self.t2.rect, pygame.Rect(0,0,32,32))
        self.assertEqual(self.t3.rect, pygame.Rect(0,0,32,32))

    def test_set_color(self):
        self.t1.redraw = False
        self.assertEqual(self.t1.redraw, False)

        self.t1.color = [0,0,0,0]
        self.assertEqual(self.t1.color, pygame.Color(0,0,0,0))
        self.assertEqual(self.t1.redraw, True)

if __name__ == '__main__':
    unittest.main()
