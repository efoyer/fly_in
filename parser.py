from .zone import Zone
from .graph import Graph
from enum import Enum


class Meta_Type(Enum):
    ZONE =  "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"


class Parser:
    b_start = False
    b_end = False
    zones: dict = {}

    @staticmethod
    def load(path: str):
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key, value = map(str.strip, line.split(":", 1))
                    Parser.type_load(key, value)

        except PermissionError as e:
            print(f"Permission Error: {e}")
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def parse_hub(line):
        if not Parser.b_start:
            try:
                name, x, y, meta = line.split(" ")
                x = int(x)
                y = int(y)
                dict_meta: dict = Parser.parse_meta(meta)


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
                if 

    




    @staticmethod
    def type_load(key: str, value: str) -> any:
        if key == "nb_drones":
            try:
                val: int = int(value)
                if val <= 0:
                    raise ValueError("NB_DRONES must be positive")
                return val
            except ValueError as e:
                print(e)

        if key == "start_hub":
            if not Parser.b_start:
                try:
                    name, x, y, meta = value.split(" ")
                    x = int(x)
                    y = int(y)
                    if name is None:
                        raise ValueError(
                            "The name cannot be None in start_hub"
                            )
                    color = meta.replace("[]", "").split("=")[1]
                    if color is not None:
                        if "color=" not in color:
                            raise ValueError("Invalid value for start_hub"
                                             "('[color=...])")
                    Parser.b_start = True
                    return Zone(name, x, y, meta)
                except ValueError as e:
                    print(e)

        if key == "end_hub":
            if not Parser.b_end:
                try:
                    name, x, y, meta = value.split(" ")
                    x = int(x)
                    y = int(y)
                    if name is None:
                        raise ValueError("The name cannot be None in end_hub")
                    color = meta.replace("[]", "").split("=")[1]
                    if color is not None and "color=" not in color:
                        raise ValueError("Invalid value for end_hub"
                                         "('[color=...])")
                    Parser.b_end = True
                    return Zone(name, x, y, meta)
                except ValueError as e:
                    print(e)

        if key == "hub":
            try:
                name, x, y, meta = value.split(" ")
                x = int(x)
                y = int(y)
                if name is None:
                    raise ValueError("The name cannot be None for hub")
                meta = meta.replace("[]", "")
                meta1, meta2, meta3 = meta.split(" ")
                for data in (meta1, meta2, meta3):
                    if "color=" in data:
                        color = data.split("=")[1]
                    if "zone=" in data:
                        zone = data.split("=")[1]
                     

            except ValueError as e:
                print(e)
