import ctypes
from ctypes import (
    POINTER,
    c_char_p,
    c_char,
    c_int,
    pointer,
    create_string_buffer,
)
import logging
import requests
import tempfile

import pandas as pd

from pychadwick.league import CWLeague
from pychadwick.game import CWGame
from pychadwick.gameiter import CWGameIterator
from pychadwick.roster import CWRoster
from pychadwick.utils import CWEventFieldStruct
from pychadwick import EVENT_DATA_TYPES, ChadwickLibrary


class Chadwick:
    FIELDS_COUNT = 96
    EXT_FIELDS_COUNT = 63

    def __init__(self, *args, **kwargs):
        self.libchadwick = ChadwickLibrary.libchadwick
        self.set_all_headers()

    def set_all_headers(self):
        [self.set_event_field(field) for field in self.all_headers]

    @property
    def all_headers(self):
        return self.cwevent_headers + self.cwevent_ext_headers

    @property
    def cwevent_headers(self):
        return [p.header.decode() for p in self.cwevent_field_data]

    @property
    def cwevent_ext_headers(self):
        return [p.header.decode() for p in self.cwevent_ext_field_data]

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

    def set_event_field(self, field_name):
        self.set_event_field_value(field_name, 1)

    def unset_event_field(self, field_name):
        self.set_event_field_value(field_name, 0)

    def set_event_field_value(self, field_name, value):
        if field_name in self.cwevent_headers:
            idx = self.cwevent_headers.index(field_name)
            self.cwevent_fields[idx] = value
        elif field_name in self.cwevent_ext_headers:
            idx = self.cwevent_ext_headers.index(field_name)
            self.cwevent_ext_fields[idx] = value
        else:
            logging.warning(
                f"field_name {field_name} is not in the headers. value NOT set"
            )

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

    def _download_to_tempfile(self, url):
        fh = tempfile.NamedTemporaryFile(delete=False)
        fh.write(requests.get(url).content)
        return fh.name

    def games(self, file_path):
        if file_path.startswith("http"):
            file_path = self._download_to_tempfile(file_path)
        file_path = bytes(str(file_path), "utf8")
        cw_game_read = self.libchadwick.cw_game_read
        cw_game_read.restype = POINTER(CWGame)
        cw_game_read.argtypes = (ctypes.c_void_p,)

        cw_file_find_first_game = self.libchadwick.cw_file_find_first_game
        cw_file_find_first_game.restype = ctypes.c_int
        cw_file_find_first_game.argtypes = (ctypes.c_void_p,)

        file_handle = self.fopen(file_path)

        cw_file_find_first_game(file_handle)
        while not self.feof(file_handle):
            yield cw_game_read(file_handle)

            # TODO: why is this here? what's the exception?
            # except:
            #     self.fclose(file_handle)
            #     return

    @property
    def active_headers(self):
        return [
            h for i, h in enumerate(self.cwevent_headers) if self.cwevent_fields[i] == 1
        ] + [
            h
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

    def cw_league_read(self, file_name):
        cw_league_init_read_file = self.libchadwick.cw_league_init_read_file
        cw_league_init_read_file.argtypes = (POINTER(CWLeague), c_char_p)
        cw_league_init_read_file.restype = None
        league = pointer(CWLeague())
        cw_league_init_read_file(league, file_name)
        return league

    def process_game_csv(self, game_ptr, roster_visitor=None, roster_home=None):
        cwevent_process_game = self.libchadwick.cwevent_process_game
        cwevent_process_game.argtypes = (
            POINTER(CWGame),
            POINTER(CWRoster),
            POINTER(CWRoster),
        )
        cwevent_process_game.restype = None

        if not roster_home:
            roster_home = pointer(CWRoster())
        if not roster_visitor:
            roster_visitor = pointer(CWRoster())

        cwevent_process_game(game_ptr, roster_visitor, roster_home)

    def process_game(self, game_ptr, roster_visitor=None, roster_home=None):
        cwevent_process_game_record = self.libchadwick.cwevent_process_game_record
        cwevent_process_game_record.argtypes = (
            POINTER(CWGameIterator),
            POINTER(CWRoster),
            POINTER(CWRoster),
            POINTER(c_char),
        )
        cwevent_process_game_record.restype = None
        gameiter = self.cw_gameiter_create(game_ptr)

        if not roster_visitor:
            logging.debug("roster for %s is undefined.", "visitor")
            roster_visitor = pointer(CWRoster())

        if not roster_home:
            logging.debug("roster for %s is undefined.", "home")
            roster_home = pointer(CWRoster())

        event_str = create_string_buffer(b" ", 4096)
        while gameiter.contents.event:
            cwevent_process_game_record(
                gameiter, roster_visitor, roster_home, event_str
            )
            self.cw_gameiter_next(gameiter)
            if event_str.value:
                yield self.dicticize_event_string(event_str.value)

    def cw_gameiter_create(self, game_ptr):
        func = self.libchadwick.cw_gameiter_create
        func.restype = POINTER(CWGameIterator)
        func.argtypes = (POINTER(CWGame),)
        return func(game_ptr)

    @staticmethod
    def convert_data_frame_types(df, data_type_mapping):
        for column_name, data_type_conversion in data_type_mapping.items():
            if column_name in df:
                try:
                    df.loc[:, column_name] = df.loc[:, column_name].astype(
                        data_type_conversion
                    )
                except TypeError:
                    print(f"Cannot convert column {column_name}")
                    print(df.loc[:column_name])
                    raise TypeError
        return df

    def games_to_dataframe(self, games, data_type_mapping=None):
        if data_type_mapping is None:
            data_type_mapping = EVENT_DATA_TYPES
        dfs = [
            pd.DataFrame(list(self.process_game(game_ptr)), dtype="f8")
            for game_ptr in games
        ]
        return self.convert_data_frame_types(
            pd.concat(dfs, axis=0, ignore_index=True), data_type_mapping
        )

    def game_to_dataframe(self, game_ptr, data_type_mapping=None):
        if data_type_mapping is None:
            data_type_mapping = EVENT_DATA_TYPES
        return self.convert_data_frame_types(
            pd.DataFrame(list(self.process_game(game_ptr)), dtype="f8"),
            data_type_mapping,
        )

    def event_file_to_dataframe(self, event_file, data_type_mapping=None):
        if data_type_mapping is None:
            data_type_mapping = EVENT_DATA_TYPES
        return self.games_to_dataframe(self.games(event_file), data_type_mapping)

    def event_files_to_dataframe(self, event_files, data_type_mapping=None):
        if data_type_mapping is None:
            data_type_mapping = EVENT_DATA_TYPES
        data = []
        for event_file in event_files:
            games = self.games(event_file)
            for game in games:
                data += list(self.process_game(game))
        return self.convert_data_frame_types(
            pd.DataFrame(data, dtype="f8"),
            data_type_mapping,
        )


    def register_function(self, func_name, func_arg_types, func_res_type):
        func = self.libchadwick.__getattr__(func_name)
        func.argtypes = func_arg_types
        func.restype = func_res_type
        self.__dict__[func_name] = func
        return func
