from ctypes import Structure, POINTER, c_char_p, c_int
from ctypes import CFUNCTYPE
from .gameiter import CWGameIterator
from .roster import CWRoster


class CWEventFieldStruct(Structure):
    pass


CWEventFieldStruct._fields_ = [
    (
        "f",
        POINTER(
            CFUNCTYPE(
                c_int, POINTER(CWGameIterator), POINTER(CWRoster), POINTER(CWRoster)
            )
        ),
    ),
    ("header", c_char_p),
    ("description", c_char_p),
]
