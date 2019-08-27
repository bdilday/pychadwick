import ctypes
from ctypes import Structure, POINTER, c_char, c_char_p, c_int
from ctypes import CFUNCTYPE
from .game import CWComment, CWGame


class CWScorebook(Structure):
    pass


class CWScorebookIterator(Structure):
    pass


CWScorebook._fields_ = [
    ("first_comment", POINTER(CWComment)),
    ("last_comment", POINTER(CWComment)),
    ("first_game", POINTER(CWGame)),
    ("last_game", POINTER(CWGame)),
]


CWScorebookIterator._fields_ = [
    ("current", POINTER(CWGame)),
    ("f", POINTER(CFUNCTYPE(c_int, POINTER(CWGame)))),
]

