# /usr/bin/python3

import os
import sys
sys.path.append(os.pardir)

from nodes import Nodes


FULL_TABLE = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "D"],
    "D": ["B", "C"],
    "E": ["B"]}

UPDATE_TABLE = {
    "A": ["C", "D"],
    "B": ["A", "E"]}

node_data = Nodes()
node_data.update_route_table(FULL_TABLE)


def test_get_paths_num(node_data):
    node_data.update_route_table(FULL_TABLE)
    assert 5 == node_data.get_paths_num()


def test_get_shortest_path():
    # Illyaaaaaaaaaaaaaa
    pass


test_get_paths_num(node_data)
