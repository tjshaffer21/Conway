#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import conway
from conway import tilemap

class TestTileMethods(unittest.TestCase):

    def test_set_color(self):
        tile = tilemap.Tile()
        tile.color = [0, 0, 0, 0]
        self.assertEqual(tile.color, [0, 0, 0, 0], "incorrect color")

    def test_set_texture(self):
        tile = tilemap.Tile()
        tile.texture = 2415
        self.assertEqual(tile.texture, 2415, "incorrect id")


class TestTileMapMethods(unittest.TestCase):

    def setUp(self):
        self.tilemap = tilemap.TileMap(10, 10, 2)

    def test_init(self):
        self.assertEqual(self.tilemap.chunk_width, 10, "incorrect chunk width")
        self.assertEqual(self.tilemap.chunk_height, 10, "incorrect chunk height")
        self.assertEqual(self.tilemap.chunk_size, [10,10], "incorrect chunk size")
        self.assertEqual(self.tilemap.current_chunk, 1, "incorrect current chunk.")

        self.assertEqual(self.tilemap.tile_size, [32, 32], "incorrect tile size")
        self.assertEqual(self.tilemap.tile_width, 32, "incorrect tile width")
        self.assertEqual(self.tilemap.tile_height, 32, "incorrect tile height")

    def test_chunk_change(self):
        self.tilemap.current_chunk = 2
        self.assertEqual(self.tilemap.current_chunk, 2, "incorrect chunk")

        with self.assertRaises(ValueError):
            self.tilemap.current_chunk = 3

            
if __name__ == '__main__':
    unittest.main()
