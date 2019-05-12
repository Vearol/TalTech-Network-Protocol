#! /usr/bin/python3

from global_config import INIT_NODES, SERVER_KEY, MAX_ROUTE_COST
from colors import colors
from byte_parser import bytes_to_number, bytes_to_GPG


class Nodes:

    def __init__(self, host_id=SERVER_KEY):
        self.host_id = host_id
        self.tables = [{host_id: {host_id: 0}}]
        self.nodes_data = INIT_NODES
        self.nicknames = {}

    def set_network_info(self, key, ip, port):
        if key not in self.nodes_data.keys():
            self.nodes_data[key] = [0, 0, 0]
        self.nodes_data[key][0] = ip
        self.nodes_data[key][1] = port

    def get_key_by_nickname(self, nickname):
        for key, value in self.nodes_data.items():
            if value[2] == nickname:
                return key

        log = "Not able to find GPG key for nickname: " + nickname
        print(colors.ERROR, log)
        return None

    def get_neighbors(self):
        keys = []
        for key in self.nodes_data.keys():
            if (key != SERVER_KEY):
                keys.append(key)
        return keys

    def get_all_nodes(self):
        all_nodes = []
        for table in self.tables:
            for node in table.keys():
                if node not in all_nodes:
                    all_nodes.append(node)

            for node in table.values():
                if node not in all_nodes:
                    all_nodes.append(node)

        return all_nodes

    def get_network_info(self, key):
        key = key.lower()
        if key in self.nodes_data.keys():
            ip = self.nodes_data[key][0]
            port = self.nodes_data[key][1]
            return (ip, port)
        else:
            return (None, None)

    def set_nickname(self, key, nickname):
        if key in self.nodes_data.keys():
            self.nodes_data[key][2] = nickname
        self.nicknames[key] = nickname

    def get_nickname(self, key):
        if key in self.nodes_data.keys():
            return self.nodes_data[key][2]
        if key in self.nicknames.keys():
            return self.nicknames[key]
        return ""

    def get_unknown_nodes(self):
        all_nodes = self.get_all_nodes()
        unknown_nodes = []
        for node in all_nodes:
            if (self.get_nickname(node) == ""):
                unknown_nodes.append(node)
        return unknown_nodes

    def is_updated(self, src_id, table_byte, cost=0):
        table = self.byte_to_table(table_byte, cost)
        if table in self.tables:
            return True
        else:
            return False

    def update_table(self, src_id, table_byte, cost=0):
        self.remove_table(src_id)
        self.add_table_byte(table_byte, cost=0)

    def add_table_byte(self, table_byte, cost=0):
        table = self.byte_to_table(table_byte, cost)
        self.tables.append(table)

    def byte_to_table(self, table_byte, cost=0):
        array = []
        table = {}
        table_key = ''
        for x in range(int(len(table_byte) / 10)):
            array.append(table_byte[:10])
        for a in array:
            key = bytes_to_GPG(a[:8])
            value = bytes_to_number(a[8:])
            if value == MAX_ROUTE_COST:
                continue
            table[key] = value + cost
            if value == 0:
                table_key = key
        return {table_key: table}

    def remove_table(self, src_id):
        for idx, table in enumerate(self.tables):
            if src_id in table.keys():
                self.tables.pop(idx)

    def get_full_table_byte(self):
        ret = b""
        full_table = self.get_full_table()
        for key, value in sorted(full_table.items()):
            str_value = str(value)
            ret += bytes(key)
            ret += bytes(str_value.zfill(2))
        return ret

    def get_full_table(self):
        full_table = {}
        tables = self.tables
        for table in tables:
            if self.host_id in table.keys():
                continue
            for src_id, routes in table.items():
                for dest_id, cost in routes.items():
                    if dest_id not in full_table.keys():
                        full_table[dest_id] = cost
                    elif full_table[dest_id] > cost:
                        full_table[dest_id] = cost
        return full_table

    def get_nearest_neighbor(self, dest_id):
        if (dest_id in self.nodes_data.keys()):
            return dest_id

        tables = self.tables
        key = ''
        min_cost = float('inf')
        for table in tables:
            for table_key, table_value in table.items():
                for k, v in table_value.items():
                    if k == dest_id and v < min_cost:
                        min_cost = v
                        key = table_key
        return key

    def clear_tables(self):
        self.tables = [{self.host_id: {self.host_id: 0}}]
