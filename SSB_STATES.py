from enum import Enum


class States(Enum):
    BUSY = -1
    START = 0
    UPLOAD = 1
    DETECT = 2
    MATCH = 3
    MODIFY = 4
    MODIFY_MATCHES = 5


