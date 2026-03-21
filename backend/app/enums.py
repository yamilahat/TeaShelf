from enum import Enum


class TeaType(str, Enum):
    green = "green"
    white = "white"
    black = "black"
    red = "red"
    yellow = "yellow"
    oolong = "oolong"
    ripe_puerh = "ripe pu-erh"
    raw_puerh = "raw pu-erh"
