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

import pandas as pd

from .game import CWGame
from .gameiter import CWGameIterator
from .roster import CWRoster
from .utils import CWEventFieldStruct


class Chadwick:
    FIELDS_COUNT = 96
    EXT_FIELDS_COUNT = 63

    def __init__(self, library_path="libchadwick2.so", *args, **kwargs):
        self._dll = None
        self.library_path = library_path
        self._load_shared_library(library_path)

    @property
    def cwevent_headers(self):
        return [p.header for p in self.cwevent_field_data]

    @property
    def cwevent_ext_headers(self):
        return [p.header for p in self.cwevent_ext_field_data]

    @property
    def cwevent_field_data(self):
        p = CWEventFieldStruct * self.FIELDS_COUNT
        return p.in_dll(self.libchadwick, "cwevent_field_data")

    @property
    def cwevent_fields(self):
        p = c_int * self.FIELDS_COUNT
        return p.in_dll(self.libchadwick, "fields")

    @property
    def cwevent_ext_field_data(self):
        p = CWEventFieldStruct * self.EXT_FIELDS_COUNT
        return p.in_dll(self.libchadwick, "cwevent_ext_field_data")

    @property
    def cwevent_ext_fields(self):
        p = c_int * self.EXT_FIELDS_COUNT
        return p.in_dll(self.libchadwick, "ext_fields")

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
        file_handle = self.fopen(file_path)
        while not self.feof(file_handle):
            try:
                yield cw_game_read(file_handle)
            except:
                self.fclose(file_handle)
                return

    @property
    def active_headers(self):
        return [
            h.decode()
            for i, h in enumerate(self.cwevent_headers)
            if self.cwevent_fields[i] == 1
        ] + [
            h.decode()
            for i, h in enumerate(self.cwevent_ext_headers)
            if self.cwevent_ext_fields[i] == 1
        ]

    def dicticize_event_string(self, event_bytes, headers=None):
        if headers is None:
            headers = self.active_headers

        return dict(zip(headers, self.listicize_event_string(event_bytes)))

    @staticmethod
    def listicize_event_string(event_bytes):
        return [
            event_item.replace(r'"', "")
            for event_item in event_bytes.decode().split(",")
        ]

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
            self.cw_gameiter_next(gi)
            yield self.dicticize_event_string(s.value)

    def cw_gameiter_create(self, game_ptr):
        func = self.libchadwick.cw_gameiter_create
        func.restype = POINTER(CWGameIterator)
        func.argtypes = (POINTER(CWGame),)
        return func(game_ptr)

    def game_to_dataframe(self, game_ptr):
        return pd.DataFrame(list(self.process_game(game_ptr)), dtype='f8')