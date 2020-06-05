from ctypes import Structure, POINTER
from .roster import CWRoster


class CWLeague(Structure):
    pass


CWLeague._fields_ = [
    ("first_roster", POINTER(CWRoster)),
    ("last_roster", POINTER(CWRoster)),
]
