#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import conway
from conway import camera

class TestCameraMethods(unittest.TestCase):

    def setUp(self):
        self.cam = camera.Camera()

    def test_init(self):
        self.assertEqual(self.cam.viewport, [100,100], "incorrect viewport")
        self.assertEqual(self.cam.position, [0,0], "incorrect position")
        self.assertEqual(self.cam.x, 0, "incorrect x")
        self.assertEqual(self.cam.y, 0, "incorrect y")

        self.cam.x = 10
        self.cam.y = 15
        self.assertEqual(self.cam.x, 10, "incorrect x")
        self.assertEqual(self.cam.y, 15, "incorrect y")

        self.assertEqual(self.cam.zoom, 1.0, "incorrect zoom")
        self.cam.zoom = 0.5
        self.assertEqual(self.cam.zoom, 0.5, "incorrect zoom")

        self.cam.move([20, 0])
        self.assertEqual(self.cam.position, [20,0], "incorrect position")

        self.cam.resize([50,50])
        self.assertEqual(self.cam.viewport, [50,50], "incorrect viewport")

if __name__ == '__main__':
    unittest.main()
