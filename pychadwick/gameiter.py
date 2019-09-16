import ctypes
from ctypes import Structure, POINTER, c_char, c_char_p, c_int
from .game import CWGame, CWEvent
from .parse import CWEventData


class CWGameState(Structure):
    pass


class CWGameIterator(Structure):
    pass


class LINEUP(Structure):
    _fields_ = [("player_id", c_char_p), ("name", c_char_p), ("position", c_int)]


CWGameState._fields_ = [
    ("date", c_char * 9),
    ("event_count", c_int),
    ("inning", c_int),
    ("batting_team", c_int),
    ("outs", c_int),
    ("inning_batters", c_int),
    ("inning_score", c_int),
    ("score", c_int * 2),
    ("hits", c_int * 2),
    ("errors", c_int * 2),
    ("times_out", c_int * 2),
    ("next_batter", c_int * 2),
    ("num_batters", c_int * 2),
    ("dh_slot", c_int * 2),
    ("num_itb_runners", c_int * 2),
    ("is_leadoff", c_int),
    ("is_new_pa", c_int),
    ("ph_flag", c_int),
    ("runners", (c_char * 50) * 4),
    ("pitchers", (c_char * 50) * 4),
    ("catchers", (c_char * 50) * 4),
    ("runner_src_event", c_int * 4),
    ("lineups", (LINEUP * 2) * 10),
    ("fielders", (POINTER(c_char) * 2) * 10),
    ("removed_for_ph", c_char_p),
    ("removed_for_pr", c_char_p * 4),
    ("walk_pitcher", c_char_p),
    ("strikeout_batter", c_char_p),
    ("removed_position", c_int),
    ("go_ahead_rbi", c_char_p),
    ("batter_hand", c_char),
]

CWGameIterator._fields_ = [
    ("game", POINTER(CWGame)),
    ("event", POINTER(CWEvent)),
    ("event_data", POINTER(CWEventData)),
    ("parse_ok", c_int),
    ("state", POINTER(CWGameState)),
]
