# /usr/bin/python3

import os
import unittest
import sys
sys.path.append(os.pardir)

from nodes import Nodes


class TestNodes(unittest.TestCase):

    def test_add_table_byte(self):
        nodes = Nodes()
        EXPECTED = [{"nodeself": {"nodeself": 0}},
                    {"BBBBBBBB": {"BBBBBBBB": 1}}]
        ARG1 = bytearray("\x42\x42\x42\x42\x42\x42\x42\x42\x30\x30")
        ARG2 = 1
        nodes.add_table_byte(ARG1, ARG2)
        actual = nodes.tables
        self.assertEqual(EXPECTED, actual)

    def test_remove_table(self):
        nodes = Nodes()
        nodes.tables.append({"BBBBBBBB": {"BBBBBBBB": 1}})
        EXPECTED = [{"nodeself": {"nodeself": 0}}]
        ARG1 = "BBBBBBBB"
        nodes.remove_table(ARG1)
        actual = nodes.tables
        self.assertEqual(EXPECTED, actual)

    def test_get_full_table(self):
        nodes = Nodes()
        TABLES = [{"BBBBBBBB": {"BBBBBBBB": 1,
                                "CCCCCCCC": 4,
                                "DDDDDDDD": 2,
                                "EEEEEEEE": 3}},
                  {"CCCCCCCC": {"BBBBBBBB": 4,
                                "CCCCCCCC": 1,
                                "DDDDDDDD": 3,
                                "EEEEEEEE": 2}}]
        nodes.tables.extend(TABLES)
        EXPECTED = {"BBBBBBBB": 1,
                    "CCCCCCCC": 1,
                    "DDDDDDDD": 2,
                    "EEEEEEEE": 2}
        actual = nodes.get_full_table()
        self.assertEqual(EXPECTED, actual)

    def test_get_full_table_byte(self):
        nodes = Nodes()
        TABLES = [{"BBBBBBBB": {"BBBBBBBB": 1,
                                "CCCCCCCC": 4,
                                "DDDDDDDD": 2,
                                "EEEEEEEE": 3}},
                  {"CCCCCCCC": {"BBBBBBBB": 4,
                                "CCCCCCCC": 1,
                                "DDDDDDDD": 3,
                                "EEEEEEEE": 2}}]
        nodes.tables.extend(TABLES)
        EXPECTED = b"\x42\x42\x42\x42\x42\x42\x42\x42\x30\x31"
        EXPECTED += b"\x43\x43\x43\x43\x43\x43\x43\x43\x30\x31"
        EXPECTED += b"\x44\x44\x44\x44\x44\x44\x44\x44\x30\x32"
        EXPECTED += b"\x45\x45\x45\x45\x45\x45\x45\x45\x30\x32"
        actual = nodes.get_full_table_byte()
        self.assertEqual(EXPECTED, actual)

    def test_get_nearest_neighbor(self):
        nodes = Nodes()
        TABLES = [{"BBBBBBBB": {"BBBBBBBB": 1,
                                "CCCCCCCC": 4,
                                "DDDDDDDD": 2,
                                "EEEEEEEE": 3}},
                  {"CCCCCCCC": {"BBBBBBBB": 4,
                                "CCCCCCCC": 1,
                                "DDDDDDDD": 3,
                                "EEEEEEEE": 2}}]
        TARGET = "EEEEEEEE"
        nodes.tables.extend(TABLES)
        EXPECTED = "CCCCCCCC"
        actual = nodes.get_nearest_neighbor(TARGET)
        self.assertEqual(EXPECTED, actual)


if __name__ == "__main__":
    unittest.main()
