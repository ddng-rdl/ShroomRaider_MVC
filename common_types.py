# pyright: strict

from enum import Enum, auto


class Tile(Enum):
    LARO = ("L", "\N{ADULT}")
    TREE = ("T", "\N{EVERGREEN TREE}")
    MUSHROOM = ("+", "\N{MUSHROOM}")
    WATER = ("~", "\N{LARGE BLUE SQUARE}")
    ROCK = ("R", "🌑")
    PAVED = ("-", "\N{WHITE LARGE SQUARE}")
    EMPTY = (".", "\u3000")
    AXE = ("x", "\N{AXE}")
    FLAMETHROWER = ("*", "\N{FIRE}")

    def __init__(self, ascii: str, emoji: str) -> None:
        self.ascii = ascii
        self.emoji = emoji


UI: dict[str, str] = {tile.ascii: tile.emoji for tile in Tile}


class GameEvent(Enum):
    NONE = auto()
    OUT_OF_BOUNDS = auto()
    MUSHROOM_COLLECTED = auto()
    DROWNED = auto()
    ITEM_FOUND = auto()
    TREE_BLOCKED = auto()
    ROCK_OUT_OF_BOUNDS = auto()
    ROCK_BLOCKED = auto()
    WATER_PAVED = auto()
    ROCK_PUSHED = auto()
    INVALID_ROCK_PUSH = auto()
    TREE_CHOPPED = auto()
    TREE_BURNED = auto()
    NO_LARO = auto()
    PICKED_AXE = auto()
    PICKED_FLAMETHROWER = auto()
    ALREADY_HOLDING = auto()
    NOTHING_TO_PICKUP = auto()
    STAGE_RESET = auto()
