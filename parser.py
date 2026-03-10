from .hub import Hub
from .graph import Graph
from enum import Enum
from .connection import Connection


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

    @staticmethod
    def load(path: str) -> Graph:
        try:
            Parser.hubs = []
            with open(path, "r") as f:
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
                        Parser.hubs.append(hub)
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
                             hubs=Parser.hubs,
                             connection=lst_con)
        except PermissionError as e:
            print(f"Permission Error: {e}")
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def parse_nb_drones(line: str) -> int:
        try:
            line.strip()
            value: int = int(line)
            if value >= 0:
                return value
            else:
                raise ValueError(f"nb_drones cannot be negative: {value}")
        except Exception as e:
            print(e)

    def parse_connection(line) -> Connection:
        try:
            hub1, hub2 = line.split("-")
            if not Parser.is_valid_hub(hub1):
                raise ValueError(f"Line: {line}. {hub1} isn't a valid hub !")
            if not Parser.is_valid_hub(hub2):
                raise ValueError(f"Line: {line}. {hub2} isn't a valid hub !")
            connex = Connection(Parser.name_to_hub(hub1),
                                Parser.name_to_hub(hub2))
            return connex

        except Exception as e:
            print(e)

    def parse_hub(line) -> Hub:
        try:
            name, x, y, meta = line.split(" ")
            x = int(x)
            y = int(y)
            if meta:
                dict_meta: dict = Parser.parse_meta(meta)
                return Hub(name, x, y, dict_meta)
            return Hub(name, x, y)
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
                    if value in (c.value for c in Color):
                        color = value
                    else:
                        raise ValueError(f"{value} isn't a valid color !")
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

    def is_valid_hub(name: str) -> bool:
        for hub in Parser.hubs:
            if hub.get_name() == name:
                return True
        return False

    def name_to_hub(name: str) -> Hub:
        if not Parser.is_valid_zone(name):
            raise ValueError(f"{name} isn't a hub (name_to_hub)")
        for hub in Parser.hubs:
            if hub.get_name() == name:
                return hub
        raise ValueError("No Hub found ! (name_to_hub function)")
