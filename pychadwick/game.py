import ctypes
from ctypes import Structure, POINTER, c_char, c_char_p, c_int


class CWInfo(Structure):
    pass


class CWAppearance(Structure):
    pass


class CWComment(Structure):
    pass


class CWEvent(Structure):
    pass


class CWData(Structure):
    pass


class CWGame(Structure):
    pass


CWInfo._fields_ = [
    ("label", c_char_p),
    ("data", c_char_p),
    ("prev", POINTER(CWInfo)),
    ("next", POINTER(CWInfo)),
]

CWAppearance._fields_ = [
    ("player_id", c_char_p),
    ("name", c_char_p),
    ("team", c_int),
    ("slot", c_int),
    ("pos", c_int),
    ("prev", POINTER(CWAppearance)),
    ("next", POINTER(CWAppearance)),
]

CWComment._fields_ = [
    ("text", c_char_p),
    ("prev", POINTER(CWComment)),
    ("next", POINTER(CWComment)),
]

CWEvent._fields_ = [
    ("inning", c_int),
    ("batting_team", c_int),
    ("batter", c_char_p),
    ("count", c_char_p),
    ("pitches", c_char_p),
    ("event_text", c_char_p),
    ("batter_hand", c_char),
    ("pitcher_hand", c_char),
    ("pitcher_hand_id", c_char_p),
    ("ladj_align", c_int),
    ("ladj_slot", c_int),
    ("itb_base", c_int),
    ("itb_runner_id", c_char_p),
    ("first_sub", POINTER(CWAppearance)),
    ("last_sub", POINTER(CWAppearance)),
    ("first_comment", POINTER(CWComment)),
    ("last_comment", POINTER(CWComment)),
    ("prev", POINTER(CWEvent)),
    ("next", POINTER(CWEvent)),
]

CWData._fields_ = [
    ("num_data", c_int),
    ("data", POINTER(POINTER(c_char))),
    ("prev", POINTER(CWData)),
    ("next", POINTER(CWData)),
]

CWGame._fields_ = [
    ("game_id", c_char_p),
    ("version", c_char_p),
    ("first_info", POINTER(CWInfo)),
    ("last_info", POINTER(CWInfo)),
    ("first_starter", POINTER(CWAppearance)),
    ("last_starter", POINTER(CWAppearance)),
    ("first_event", POINTER(CWEvent)),
    ("last_event", POINTER(CWEvent)),
    ("first_data", POINTER(CWData)),
    ("last_data", POINTER(CWData)),
    ("first_stat", POINTER(CWData)),
    ("last_stat", POINTER(CWData)),
    ("first_line", POINTER(CWData)),
    ("last_line", POINTER(CWData)),
    ("first_evdata", POINTER(CWData)),
    ("last_evdata", POINTER(CWData)),
    ("first_comment", POINTER(CWComment)),
    ("last_comment", POINTER(CWComment)),
    ("prev", POINTER(CWGame)),
    ("next", POINTER(CWGame)),
]

