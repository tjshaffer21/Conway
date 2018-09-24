#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, pygame
from conway.ui import ui_object

class TestUIObject(unittest.TestCase):
    def test_rect(self):
        ui1 = ui_object.UIObject([0,0,10,10])
        self.assertEqual(ui1.rect, pygame.Rect(0,0,10,10))

        ui2 = ui_object.UIObject(pygame.Rect(0,0,100,100))
        self.assertEqual(ui2.rect, pygame.Rect(0,0,100,100))

if __name__ == '__main__':
    unittest.main()