"""Module responsible for parsing the map configuration file into a Graph."""

from src.hub import Hub
from src.graph import Graph
from enum import Enum
from src.connection import Connection
from typing import TypedDict
import sys


class Meta_Type(Enum):
    ZONE = "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"


class Zone_Type(Enum):
    RESTRICTED = "restricted"
    NORMAL = "normal"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class MetaDict(TypedDict):
    color: str | None
    zone: str
    max_drones: int


class Parser:
    """Parse a map file and construct a Graph object from it.

    The Parser reads a key-value text file defining hubs, connections,
    and simulation parameters. It validates all entries and raises
    descriptive errors on malformed input.
    """

    hubs: list[Hub] = []
    lst_con: list[Connection] = []

    @staticmethod
    def load(path: str) -> Graph:
        """Parse a map file and return a fully constructed Graph.

        Reads the file line by line, dispatching each key-value pair
        to the appropriate sub-parser. Validates that a start hub,
        end hub, and drone count are all present, and that the end
        hub is reachable via at least one connection.

        Args:
            path: Filesystem path to the map configuration file.

        Returns:
            A Graph object populated with all hubs and connections
            defined in the file.

        Raises:
            SystemExit: On any file, permission, or validation error.
        """
        try:
            b_start = False
            b_end = False
            b_drones = False
            Parser.hubs = []
            Parser.lst_con = []
            start: Hub | None = None
            end: Hub | None = None
            nb_drones: int | None = None
            with open(path, "r") as f:
                i: int = 0
                l: int = 1
                for line in f:
                    line = line.strip()
                    i += 1
                    if not line or line.startswith('#'):
                        continue
                    if ":" not in line:
                        raise ValueError(f"Line {i}: A line must contain"
                                         " (':') \nReminder of the "
                                         "request structure: <key: value>")
                    key, value = map(str.strip, line.split(":", 1))
                    if key != "nb_drones" and l == 1:
                        raise ValueError(f"Line: {i}: "
                                         "The file must begin with nb_drones")
                    if key == "start_hub" and not b_start:
                        start = Parser.parse_hub(value, i)
                        if start is not None:
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
                        raise ValueError(f"Line {i}: {key} isn't a valid key !"
                                         "\nValid key : nb_drones, start_hub, "
                                         "end_hub, hub, connection")
                    l += 1
                Parser.check_var(end, nb_drones)
                if not Parser.check_to_end(end):
                    raise ValueError("ValueError: There are no connections "
                                     "linked to the output")
                assert nb_drones is not None
                assert start is not None
                assert end is not None
                return Graph(nb_drones=nb_drones,
                             start=start,
                             end=end,
                             hubs=Parser.hubs,
                             connection=Parser.lst_con)
        except PermissionError as e:
            print(f"Permission Error: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")
            sys.exit(1)
        except ValueError as e:
            print(e)
            sys.exit(1)
        except IsADirectoryError:
            print(f"<{path}> is a directory !")
            sys.exit(1)
        except Exception as e:
            print(f"Error at line {i}: {e}")
            sys.exit(1)

    @staticmethod
    def parse_nb_drones(line: str, n_line: int) -> int:
        """Parse and validate the nb_drones value from a line string.

        Args:
            line: The raw value string after the 'nb_drones:' key.
            n_line: The line number in the file, used for error messages.

        Returns:
            A positive integer representing the number of drones.

        Raises:
            Exception: If the value is not a positive integer.
        """

        try:
            line = line.strip()
            value: int = int(line)
            if value > 0:
                return value
            else:
                raise ValueError(f"Line {n_line}: "
                                 f"nb_drones cannot be negative: {value}")
        except Exception as e:
            raise Exception(f"Exception at line {n_line}: {e}")

    @staticmethod
    def parse_connection(line: str, n_line: int) -> Connection:
        """Parse a connection definition and return a Connection object.

        Accepts the format 'hub1-hub2' or 'hub1-hub2 [max_link_capacity=N]'.
        Validates that both hubs exist, are distinct, and that the connection
        does not already exist.

        Args:
            line: The raw value string after the 'connection:' key.
            n_line: The line number in the file, used for error messages.

        Returns:
            A Connection object linking the two named hubs.

        Raises:
            ValueError: If either hub is unknown, hubs are identical,
                the connection already exists, or capacity is below 1.
            Exception: On any other parsing failure.
        """
        try:
            hub1: str
            hub2: str
            max_cap: int = 1
            if "[" in line and "]" in line:
                meta: str | None
                connection, meta = line.split(" ")
                hub1, hub2 = connection.split("-")
                meta = meta.replace("[", "").replace("]", "")
                key, value = meta.split("=")
                if key == "max_link_capacity":
                    max_cap = int(value)
                    if max_cap < 1:
                        raise ValueError(f"Line {n_line}: "
                                         "max_link_capacity < 1")
            else:
                hub1, hub2 = line.split("-")
            if not Parser.is_valid_hub(hub1):
                raise ValueError(f"{line}. {hub1} isn't a valid hub !")
            if not Parser.is_valid_hub(hub2):
                raise ValueError(f"{line}. {hub2} isn't a valid hub !")
            if hub1 == hub2:
                raise ValueError("Two arguments have "
                                 "the same name (connection)")
            for c in Parser.lst_con:
                if (c.get_str() == f"{hub1}-{hub2}" or
                   c.get_str() == f"{hub2}-{hub1}"):
                    raise ValueError("Connection already exists")

            connex = Connection(Parser.name_to_hub(hub1),
                                Parser.name_to_hub(hub2), max_cap)
            return connex

        except ValueError as e:
            raise ValueError(f"ValueError at line {n_line}: {e}")
        except Exception as e:
            raise Exception(f"Exception at line {n_line}: {e}")

    @staticmethod
    def parse_hub(line: str, n_line: int) -> Hub:
        """Parse a hub definition line and return a Hub object.

        Expects the format 'name x y' or 'name x y [meta]'.
        Validates coordinate types, name uniqueness, and that the name
        does not contain a hyphen (reserved for connection syntax).

        Args:
            line: The raw value string after a 'hub:', 'start_hub:',
                or 'end_hub:' key.
            n_line: The line number in the file, used for error messages.

        Returns:
            A Hub object with the parsed name, coordinates, and metadata.

        Raises:
            ValueError: If the format is invalid, coordinates are not integers,
                the name already exists, or the name contains '-'.
            Exception: On any other parsing failure.
        """

        if "[" in line and "]" in line:
            try:
                val = line.split("[")[0].strip()
            except ValueError:
                raise ValueError(f"Line {n_line}: Error in split for value")

            try:
                meta = line.split("[")[1].split("]")[0]
            except ValueError:
                raise ValueError(f"Line {n_line}: Error in split for meta")

            try:
                name, x_str, y_str = val.split(" ")
            except ValueError:
                raise ValueError(f"Line {n_line}: The line should be: "
                                 "name, x, y [optional meta]")
        else:
            try:
                name, x_str, y_str = line.split(" ")
            except ValueError:
                raise ValueError(f"Line {n_line}: The line should be: "
                                 "name, x, y [optional meta]")
            meta = None
        try:
            x = int(x_str)
        except ValueError:
            raise ValueError(f"Line {n_line}: '{x}' isn't a integer")
        try:
            y = int(y_str)
        except ValueError:
            raise ValueError(f"Line {n_line}: '{y}' isn't a integer")
        try:
            if x is None or y is None:
                raise ValueError(f'Line {n_line}: x, y must not be None')
            if name in (h.get_name() for h in Parser.hubs):
                raise ValueError(f"Line {n_line}: {name} already exists")
            if "-" in name:
                raise ValueError(f"Line {n_line}: '-' not allowed in the name")
            if meta:
                dict_meta: MetaDict = Parser.parse_meta(meta, n_line)
                return Hub(name, x, y, dict_meta)
            return Hub(name, x, y)
        except ValueError as e:
            raise ValueError(f"ValueError at line {n_line}: {e}")
        except Exception as e:
            raise Exception(f"Error at line {n_line}: {e}")

    @staticmethod
    def parse_meta(meta: str, n_line: int) -> MetaDict:
        """Parse a metadata string and return a MetaDict.

        Processes space-separated key=value pairs within square brackets.
        Valid keys are 'color', 'zone', and 'max_drones'.

        Args:
            meta: The raw metadata string, e.g. 'color=blue zone=restricted'.
            n_line: The line number in the file, used for error messages.

        Returns:
            A MetaDict with validated color, zone, and max_drones values.

        Raises:
            ValueError: If any key is invalid, the zone type is unknown,
                or max_drones is not a non-negative integer.
        """
        res: MetaDict = {
            "color": None,
            "zone": "normal",
            "max_drones": 1
        }
        meta = meta.replace("[", "").replace("]", "")
        meta = meta.strip()
        for data in meta.split(" "):
            key, value = data.split("=", 1)
            if key in (e.value for e in Meta_Type):
                if key == "color":
                    color = value
                    if color == "rainbow":
                        color = "cyan"
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
                        raise ValueError(f"Line {n_line}: {e}")
                else:
                    raise ValueError(f"Line {n_line}: {key} isn't a valid key")
            else:
                raise ValueError(f"Line {n_line}: {key} isn't a valid key")
        return res

    @staticmethod
    def is_valid_hub(name: str) -> bool:
        for hub in Parser.hubs:
            if hub.get_name() == name:
                return True
        return False

    @staticmethod
    def name_to_hub(name: str) -> Hub:
        if not Parser.is_valid_hub(name):
            raise ValueError(f"{name} isn't a hub (name_to_hub)")
        for hub in Parser.hubs:
            if hub.get_name() == name:
                return hub
        raise ValueError("No Hub found ! (name_to_hub function)")

    @staticmethod
    def check_var(end: Hub | None, nb_drones: int | None) -> None:
        if end is None:
            raise ValueError("end_hub does not exist")
        if nb_drones is None:
            raise ValueError("nb_drones does not exist")

    @staticmethod
    def check_to_end(end: Hub | None) -> bool:
        for con in Parser.lst_con:
            if con.end == end:
                return True
        return False

    @staticmethod
    def check_begin_con(start: Hub) -> bool:
        for con in Parser.lst_con:
            if con.start == start:
                return True
        return False
