# /usr/bin/python3

import os
import sys
sys.path.append(os.pardir)

from nodes import Nodes


NEIGHBORS = {'sample_gpg_id_1': '192.168.11.1',
             'sample_gpg_id_2': '192.168.11.2'}

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


def test_get_full_table(node_data):
    node_data.update_route_table(FULL_TABLE)
    assert FULL_TABLE == node_data.get_full_table()


def test_get_paths_num(node_data):
    node_data.update_route_table(FULL_TABLE)
    assert 5 == node_data.get_paths_num()


def test_update_route_table(node_data):
    node_data.update_route_table(FULL_TABLE)
    node_data.update_route_table(UPDATE_TABLE)
    assert node_data.full_table == UPDATE_TABLE


def test_get_shortest_path():
    # Illyaaaaaaaaaaaaaa
    pass


test_get_full_table(node_data)
test_get_paths_num(node_data)
test_update_route_table(node_data)
