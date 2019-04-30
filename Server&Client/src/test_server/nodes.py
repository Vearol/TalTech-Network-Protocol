#! /usr/bin/python3


class Nodes:

    def __init__(self):
        self.neighbors = {}
        self.full_table = {}

    def get_neighbors(self):
        return self.neighbors

    def get_full_table(self):
        return self.full_table

    def get_node_num(self):
        return len(self.full_table.keys())

    def get_paths_num(self):
        paths = set()
        for k in self.full_table.keys():
            for v in self.full_table[k]:
                if k == v:
                    continue
                kv = [k, v]
                kv.sort()
                paths.add(kv[0] + kv[1])
        return len(paths)

    def add_neighbor(self, node_id, address):
        if node_id not in self.neighbors.keys():
            self.neighbors.add(node_id, address)

    def remove_neighbor(self, node_id):
        self.neighbors.remove(node_id)
        return

    def update_route_table(self, table):
        self.full_table = table

    def remove_node(self, node_id):
        self.full_table.remove(node_id)

    def clear_nodes(self):
        self.neighbors = {}
        self.node_map = {}

    def get_shortest_path(self, something):
        # Illyaaaaaaaaaaaaaaa
        pass
