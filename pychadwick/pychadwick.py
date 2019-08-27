import ctypes
from ctypes import (
    Structure,
    POINTER,
    c_char,
    c_char_p,
    c_int,
    pointer,
    create_string_buffer,
)

from .game import CWGame
from .gameiter import CWGameIterator
from .roster import CWRoster
from .utils import CWEventFieldStruct


class Chadwick:
    def __init__(self, library_path="libchadwick2.so", *args, **kwargs):
        self._dll = None
        self.library_path = library_path
        self._load_shared_library(library_path)

    @property
    def cwevent_field_data(self):
        p = CWEventFieldStruct * 96
        return p.in_dll(self.libchadwick, "cwevent_field_data")

    @property
    def cwevent_fields(self):
        p = c_int * 96
        return p.in_dll(self.libchadwick, "fields")

    @property
    def libchadwick(self):
        if self._dll is None:
            self._load_shared_library(self.library_path)
        return self._dll

    def _load_shared_library(self, library_path):
        self._dll = ctypes.cdll.LoadLibrary(library_path)

    def fopen(self, file_path, mode=b"r"):
        func = self.libchadwick.fopen
        func.argtypes = ctypes.c_char_p, ctypes.c_char_p
        func.restype = ctypes.c_void_p
        return func(file_path, mode)

    def fclose(self, file_handle):
        func = self.libchadwick.fclose
        func.argtypes = (ctypes.c_void_p,)
        func.restype = ctypes.c_int
        func(file_handle)

    def feof(self, file_handle):
        func = self.libchadwick.feof
        func.restype = c_int
        func.argtypes = (ctypes.c_void_p,)
        return func(file_handle)

    def cw_gameiter_next(self, gameiter_ptr):
        func = self.libchadwick.cw_gameiter_next
        func.restype = None
        func.argtypes = (POINTER(CWGameIterator),)
        return func(gameiter_ptr)

    def games(self, file_path):
        cw_game_read = self.libchadwick.cw_game_read
        cw_game_read.restype = POINTER(CWGame)
        cw_game_read.argtypes = (ctypes.c_void_p,)
        file_handle = self._file_open(file_path)
        while not self.feof(file_handle):
            try:
                yield cw_game_read(file_handle)
            except:
                self.fclose(file_handle)
                return

    def process_game(self, game_ptr):
        cwevent_process_game_record = self.libchadwick.cwevent_process_game_record
        cwevent_process_game_record.argtypes = (
            POINTER(CWGameIterator),
            POINTER(CWRoster),
            POINTER(CWRoster),
            POINTER(c_char),
        )
        cwevent_process_game_record.restype = None
        gi = self.cw_gameiter_create(game_ptr)
        r = CWRoster()
        rp1 = pointer(r)
        rp2 = pointer(r)
        s = create_string_buffer(b" ", 4096)
        while gi.contents.event:
            cwevent_process_game_record(gi, rp1, rp2, s)
            yield s.value

    def cw_gameiter_create(self, game_ptr):
        func = self.libchadwick.cw_gameiter_create
        func.restype = POINTER(CWGameIterator)
        func.argtypes = (POINTER(CWGame),)
        return func(game_ptr)

