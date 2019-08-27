import ctypes
from ctypes import Structure, POINTER, c_char, c_char_p, c_int
from .roster import CWRoster

class CWLeague(Structure):
    pass

CWLeague._fields_ = [
    ("first_roster", POINTER(CWRoster)),
    ("last_roster", POINTER(CWRoster)),
]

