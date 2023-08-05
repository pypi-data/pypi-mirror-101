import json
import os


class LastDB:
    def __init__(self, name):
        self.path = f"{name}.db"
        self.tables = self.load()

    def load(self):
        if os.path.isfile(self.path):
            with open(self.path) as f:
                r = json.load(f)
        else:
            d = {}
            json.dump(d, open(self.path, "w"))
            r = json.load(open(self.path, "r"))
        return r

    def dump(self):
        try:
            json.dump(self.tables, open(self.path, "w"), indent=4)
        except Exception as e:
            raise e

    def table(self, name=None):
        if name is None:
            name = "default"
        table = self.Table(self, name)
        self.tables[name] = table.dict
        self.dump()
        return table

    class Table:
        def __init__(self, out_self, name):
            self.out_self = out_self
            tables = out_self.tables
            if name in tables:
                self.dict = tables[name]
            else:
                self.dict = {}
            tables[name] = self.dict

        def insert(self, d):
            i = len(self.dict) + 1
            self.dict[str(i)] = d
            self.out_self.dump()

        def pop(self, match):
            i = self.get_index(match)
            self.dict.pop(i)
            self.out_self.dump()

        def get_index(self, match):
            for i, d in self.dict.items():
                if match[0] in d:
                    if d[match[0]] == match[1]:
                        return i
            return None

        def get(self, value, match):
            for d in self.dict.values():
                if match[0] in d:
                    if d[match[0]] == match[1]:
                        return d.get(value)
            return None

        def count(self, match):
            key, value = match
            count = 0
            for d in self.dict.values():
                if key in d:
                    if d[key] == value:
                        count += 1
            return count

        def search(self, match):
            key, value = match
            ls = []
            for d in self.dict.values():
                if key in d:
                    if d[key] == value:
                        ls.append(d)
            return ls

        def update(self, update, match):
            for d in self.dict.values():
                if match[0] in d:
                    if d[match[0]] == match[1]:
                        d[update[0]] = update[1]
                        self.out_self.dump()
                        return True
            return None

        def increment(self, k, match, i=1):
            for d in self.dict.values():
                if match[0] in d:
                    if d[match[0]] == match[1]:
                        d[k] += i
            self.out_self.dump()
            return True
