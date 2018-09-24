#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, pygame
from conway.ui import label

class TestLabelMethods(unittest.TestCase):
    def setUp(self):
        pygame.init()

        # ResourceWarning. Font closed in tearDown()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.l = label.Label("Hello World", pygame.Rect(0, 0, 0, 0),
                            self.font,
                            (0, 0, 0, 255), (0, 0, 0, 255))

    def test_text(self):
        self.assertEqual(self.l.text, "Hello World")

        self.l.text = "Goodbye world"
        self.assertEqual(self.l.text, "Goodbye world")

    def test_foreground(self):
        self.assertEqual(self.l.foreground, pygame.Color('black'))
        self.l.foreground = pygame.Color('red')
        self.assertEqual(self.l.foreground, pygame.Color('red'))

    def test_background(self):
        self.assertEqual(self.l.background, pygame.Color('black'))
        self.l.background = pygame.Color('red')
        self.assertEqual(self.l.background, pygame.Color('red'))

    def test_other_props(self):
        self.assertEqual(self.l.rect, pygame.Rect(0,0,0,0))
        self.assertEqual(self.l.antialias, 1)
        self.assertEqual(self.l._font, self.font)
        self.assertEqual(self.l._old_text_size, [0,0])
        self.assertEqual(self.l._redraw, True)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
