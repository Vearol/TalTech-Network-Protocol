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

    def get_paths_conbination(self):
        paths = set()
        for k in self.full_table.keys():
            for v in self.full_table[k]:
                if k == v:
                    continue
                kv = [k, v]
                kv.sort()
                paths.add(kv[0] + kv[1])
        return list(paths)

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
            self.neighbors[node_id] = address

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

    def get_shortest_path_data(self, base, target):
        update_history = []
        dist = {}
        graph = []
        nodes_num = self.get_node_num()
        path_list = self.get_paths_conbination()
        for points in path_list:
            graph.append([points[0], points[1]])
        for key in self.full_table.keys():
            if key == base:
                dist[key] = 0
            else:
                dist[key] = float("Inf")
        for x in range(nodes_num - 1):
            for u, v in graph:
                if dist[u] != float("Inf") and dist[u] + 1 < dist[v]:
                    update_history.append([v, u])
                    dist[v] = dist[u] + 1
        return update_history

    def get_shortest_neighbor(self, target, history):
        if target in self.neighbors.keys():
            return target
        ret = ""
        for x in reversed(history):
            if x[0] == target or ret:
                ret = x[1]
            if ret in self.neighbors.keys():
                break
        return ret
