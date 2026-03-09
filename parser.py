from .zone import Zone
from .graph import Graph
from enum import Enum
from .connection import Connection


class Meta_Type(Enum):
    ZONE =  "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"


class Zone_Type(Enum):
    RESTRICTED = "restricted"
    NORMAL = "normal"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Parser:
    @staticmethod
    def load(path: str):
        try:
            with open(path, "r") as f:
                hub: list[Zone] = []
                lst_con: list[Connection] = []
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key, value = map(str.strip, line.split(":", 1))
                    if key == "start_hub":
                        start = Parser.parse_hub(value)
                    elif key == "end_hub":
                        end = Parser.parse_hub(value)
                    elif key == "hub":
                        hub = Parser.parse_hub(value)
                        hub.append(hub)
                    elif key == "nb_drones":
                        nb_drones = Parser.parse_nb_drones(value)
                    elif key == "connection":
                        connection = Parser.parse_connection(value)
                        lst_con.append(connection)
                    else:
                        continue
                return Graph(nb_drones=nb_drones,
                             start=start,
                             end=end,
                             hubs=hub,
                             connection=lst_con)
        except PermissionError as e:
            print(f"Permission Error: {e}")
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")
        except Exception as e:
            print(f"Error: {e}")


    def parse_nb_drones(line: str):
        try:
            line.strip()
            value = int(line)
            return value
        except Exception as e:
            print(e)


    def parse_connection(line):
        pass


    def parse_hub(line):
        try:
            name, x, y, meta = line.split(" ")
            x = int(x)
            y = int(y)
            dict_meta: dict = Parser.parse_meta(meta)
            return Zone(name, x, y, dict_meta)
        except ValueError as e:
            print(e)


    def parse_meta(meta: str) -> dict:
        res = {}
        if not (meta.startswith("[") and meta.endswith("]")):
            return res  
        meta = meta.replace("[", "").replace("]", "")
        
        for data in meta.split(" "):
            key, value = data.split("=")
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
                        raise ValueError(f"{value} isn't a zone type")
                elif key == "max_drones":
                    try:
                        max_drones = int(value)
                        if max_drones < 0:
                            raise ValueError(
                                "Max drones can't be a negative value")
                        else:
                            res.update({
                                "max_drones": max_drones
                            })
                    except ValueError as e:
                        print(e)
                else:
                    raise ValueError(f"{key} isn't a valid key")
            else:
                raise ValueError(f"{key} isn't a valid key")
            return res
