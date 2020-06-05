from ctypes import Structure, POINTER, c_char, c_int


class CWPlayer(Structure):
    pass


class CWRoster(Structure):
    pass


CWPlayer._fields_ = [
    ("player_id", POINTER(c_char)),
    ("last_name", POINTER(c_char)),
    ("first_name", POINTER(c_char)),
    ("bats", c_char),
    ("throws", c_char),
]


CWRoster._fields_ = [
    ("team_id", POINTER(c_char)),
    ("city", POINTER(c_char)),
    ("nickname", POINTER(c_char)),
    ("league", POINTER(c_char)),
    ("year", c_int),
    ("first_player", POINTER(CWPlayer)),
    ("last_player", POINTER(CWPlayer)),
    ("prev", POINTER(CWRoster)),
    ("next", POINTER(CWRoster)),
]
