from hub import Hub
from graph import Graph
from enum import Enum
from connection import Connection


class Meta_Type(Enum):
    ZONE = "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"


class Zone_Type(Enum):
    RESTRICTED = "restricted"
    NORMAL = "normal"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Color(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    GRAY = "gray"
    WHITE = "white"
    BLACK = "black"
    PINK = "pink"


class Parser:
    hubs: list[Hub] = []
    lst_con: list[Connection] = []

    @staticmethod
    def load(path: str) -> Graph:
        try:
            b_start = False
            b_end = False
            b_drones = False
            Parser.hubs = []
            Parser.lst_con = []
            start = None
            end = None
            nb_drones = None
            with open(path, "r") as f:
                i: int = 0
                for line in f:
                    i += 1
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key, value = map(str.strip, line.split(":", 1))
                    if key == "start_hub" and not b_start:
                        start = Parser.parse_hub(value, i)
                        Parser.hubs.append(start)
                        b_start = True
                    elif key == "end_hub" and not b_end:
                        end = Parser.parse_hub(value, i)
                        Parser.hubs.append(end)
                        b_end = True
                    elif key == "hub":
                        hub = Parser.parse_hub(value, i)
                        Parser.hubs.append(hub)
                    elif key == "nb_drones" and not b_drones:
                        nb_drones = Parser.parse_nb_drones(value, i)
                        b_drones = True
                    elif key == "connection":
                        connection = Parser.parse_connection(value, i)
                        Parser.lst_con.append(connection)
                    elif key == "start_hub" and b_start:
                        raise ValueError(f"Line {i}: Double start")
                    elif key == "end_hub" and b_end:
                        raise ValueError(f"Line {i}: Double end")
                    elif key == "nb_drones" and b_drones:
                        raise ValueError(f"Line {i}: Double nb_drones")
                    else:
                        continue
                Parser.check_var(start, end, nb_drones)
                return Graph(nb_drones=nb_drones,
                             start=start,
                             end=end,
                             hubs=Parser.hubs,
                             connection=Parser.lst_con)
        except PermissionError as e:
            print(f"Permission Error: {e}")
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Error: {e}")

    def parse_nb_drones(line: str, n_line: int) -> int:
        try:
            line.strip()
            value: int = int(line)
            if value > 0:
                return value
            else:
                raise ValueError(f"Line {n_line}: "
                                 f"nb_drones cannot be negative: {value}")
        except Exception as e:
            print(e)

    def parse_connection(line: str, n_line: int) -> Connection:
        try:
            max: int = 1
            if "[" in line and "]" in line:
                connection, meta = line.split(" ")
                hub1, hub2 = connection.split("-")
                key, value = meta.split("=")
                if key == "max_link_capacity":
                    max = int(value)
            else:
                hub1, hub2 = line.split("-")
            if not Parser.is_valid_hub(hub1):
                raise ValueError(f"Line {n_line}: "
                                 f"{line}. {hub1} isn't a valid hub !")
            if not Parser.is_valid_hub(hub2):
                raise ValueError(f"Line {n_line}: "
                                 f"{line}. {hub2} isn't a valid hub !")
            if hub1 == hub2:
                raise ValueError(f"Line {n_line}:""Two arguments"
                                 " have the same name (connection)")
            for c in Parser.lst_con:
                if (c.get_str() == f"{hub1}-{hub2}" or
                   c.get_str() == f"{hub2}-{hub1}"):
                    raise ValueError(f"Line {n_line}: "
                                     "Connection already exists")

            connex = Connection(Parser.name_to_hub(hub1),
                                Parser.name_to_hub(hub2), max)
            return connex

        except ValueError as e:
            print(f"ValueError at line {n_line}: {e}")
        except Exception as e:
            print(f"Exception at line {n_line}: {e}")

    def parse_hub(line, n_line: int) -> Hub:
        try:
            if "[" in line and "]" in line:
                val = line.split("[")[0].strip()
                meta = line.split("[")[1].split("]")[0]
                name, x, y = val.split(" ")
            else:
                name, x, y = line.split(" ")
                meta = None
            x = int(x)
            y = int(y)

            if name in (h.get_name() for h in Parser.hubs):
                raise ValueError(f"Line {n_line}: {name} already exists")
            if "-" in name:
                raise ValueError(f"Line {n_line}: '-' not allowed in the name")
            if meta:
                dict_meta: dict = Parser.parse_meta(meta, n_line)
                return Hub(name, x, y, dict_meta)
            return Hub(name, x, y)
        except ValueError as e:
            raise ValueError(f"ValueError at line {n_line}: {e}")
        except Exception as e:
            print(f"Error at line {n_line}: {e}")

    def parse_meta(meta: str, n_line: int) -> dict:
        res = {
            "color": None,
            "zone": "normal",
            "max_drones": 1
        }
        meta = meta.replace("[", "").replace("]", "")

        for data in meta.split(" "):
            key, value = data.split("=", 1)
            if key in (e.value for e in Meta_Type):
                if key == "color":
                    color = value
                    res.update({
                        "color": color
                    })
                elif key == "zone":
                    if value in (e.value for e in Zone_Type):
                        zone = value
                        res.update({
                            "zone": zone
                        })
                    else:
                        raise ValueError(f"Line {n_line}: "
                                         f"{value} isn't a zone type")
                elif key == "max_drones":
                    try:
                        max_drones = int(value)
                        if max_drones < 0:
                            raise ValueError(f"Line {n_line}: Max drones"
                                             " can't be a negative value")
                        else:
                            res.update({
                                "max_drones": max_drones
                            })
                    except ValueError as e:
                        print(f"Line {n_line}: {e}")
                else:
                    raise ValueError(f"Line {n_line}: {key} isn't a valid key")
            else:
                raise ValueError(f"Line {n_line}: {key} isn't a valid key")
        return res

    def is_valid_hub(name: str) -> bool:
        for hub in Parser.hubs:
            if hub.get_name() == name:
                return True
        return False

    def name_to_hub(name: str) -> Hub:
        if not Parser.is_valid_hub(name):
            raise ValueError(f"{name} isn't a hub (name_to_hub)")
        for hub in Parser.hubs:
            if hub.get_name() == name:
                return hub
        raise ValueError("No Hub found ! (name_to_hub function)")

    def check_var(start: any, end: any, nb_drones: any):
        if start is None:
            raise ValueError("start_hub does not exist")
        if end is None:
            raise ValueError("end_hub does not exist")
        if nb_drones is None:
            raise ValueError("nb_drones does not exist")


if __name__ == "__main__":
    try:
        graph: Graph = Parser.load("test.txt")
        print(graph.get_infos())
    except Exception as e:
        print(f"Error: {e}")
