#! /usr/bin/python3


from global_config import INIT_NODES


class Nodes:

    def __init__(self, host_id='nodeself'):
        self.host_id = host_id
        self.tables = [{host_id: {host_id: 0}}]
        self.nodes_data = INIT_NODES

    def set_network_info(self, key, ip, port):
        self.nodes_data[key][0] = ip
        self.nodes_data[key][1] = port

    def get_network_info(self, key):
        if key in self.nodes_data.keys():
            ip = self.nodes_data[key][0]
            port = self.nodes_data[key][1]
            return [ip, port]
        else:
            return None

    def remove_network_info(self, key):
        if key in self.nodes_data.keys():
            self.nodes_data.pop(key)

    def set_nickname(self, key, nickname):
        if key in self.nodes_data.keys():
            self.nodes_data[key][2] = nickname

    def get_nickname(self, key):
        if key in self.nodes_data.keys():
            return self.nodes_data[key][2]

    def add_table_byte(self, table_byte, cost=0):
        array = []
        table = {}
        table_key = ''
        table_str = table_byte.decode()
        for x in range(len(table_str) / 10):
            array.append(table_str[:10])
        for a in array:
            key = a[:8]
            value = int(a[9:])
            table[key] = value + cost
            if value == 0:
                table_key = key
        self.tables.append({table_key: table})

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
