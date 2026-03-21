from enum import Enum


class TeaType(str, Enum):
    green = "green"
    white = "white"
    black = "black"
    red = "red"
    yellow = "yellow"
    oolong = "oolong"
    ripe_puerh = "shou pu-erh (ripe)"
    raw_puerh = "sheng pu-erh (raw)"
