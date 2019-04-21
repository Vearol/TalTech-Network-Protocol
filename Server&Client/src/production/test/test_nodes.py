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
node_data.add_neighbor("B", "xxx.xxx.xxx.xxx")
node_data.add_neighbor("C", "yyy.yyy.yyy.yyy")


def test_get_paths_num(node_data):
    assert 5 == node_data.get_paths_num()


def test_get_shortest_neighbor(node_data, base, target):
    history = node_data.get_shortest_path_data("A", target)
    test = node_data.get_shortest_neighbor(target, history)
    assert "B" == test


test_get_paths_num(node_data)
# test_get_shortest_neighbor(node_data, "A", "F")
test_get_shortest_neighbor(node_data, "A", "E")
