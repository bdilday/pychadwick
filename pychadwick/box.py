import ctypes
from ctypes import Structure, POINTER, c_char, c_char_p, c_int


class CWBoxBatting(Structure):
    pass

class CWBoxFielding(Structure):
    pass


class CWBoxPlayer(Structure):
    pass


class CWBoxPitching(Structure):
    pass


class CWBoxPitcher(Structure):
    pass




class CWBoxEvent(Structure):
    pass


class CWBoxscore(Structure):
    pass


CWBoxBatting._fields_ = [
    ("g", c_int),
    ("pa", c_int),
    ("ab", c_int),
    ("r", c_int),
    ("h", c_int),
    ("b2", c_int),
    ("b3", c_int),
    ("hr", c_int),
    ("hrslam", c_int),
    ("bi", c_int),
    ("bi2out", c_int),
    ("gw", c_int),
    ("bb", c_int),
    ("ibb", c_int),
    ("so", c_int),
    ("gdp", c_int),
    ("hp", c_int),
    ("sh", c_int),
    ("sf", c_int),
    ("sb", c_int),
    ("cs", c_int),
    ("xi", c_int),
    ("lisp", c_int),
    ("movedup", c_int),
    ("pitches", c_int),
    ("strikes", c_int),
]

CWBoxFielding._fields_ = [
    ("g", c_int),
    ("outs", c_int),
    ("bip", c_int),
    ("bf", c_int),
    ("po", c_int),
    ("a", c_int),
    ("e", c_int),
    ("dp", c_int),
    ("tp", c_int),
    ("pb", c_int),
    ("xi", c_int),
]

CWBoxPlayer._fields_ = [
    ("player_id", c_char_p),
    ("name", c_char_p),
    ("date", c_char * 9),
    ("battiing", POINTER(CWBoxBatting)),
    ("ph_inn", c_int),
    ("pr_inn", c_int),
    ("num_positions", c_int),
    ("start_position", c_int),
    ("positions", c_int * 40),
    ("fielding", POINTER(CWBoxFielding) * 10),
    ("prev", POINTER(CWBoxPlayer)),
    ("next", POINTER(CWBoxPlayer)),
]


CWBoxPitching._fields_ = [
    ("g", c_int),
    ("gs", c_int),
    ("cg", c_int),
    ("sho", c_int),
    ("gf", c_int),
    ("outs", c_int),
    ("ab", c_int),
    ("r", c_int),
    ("er", c_int),
    ("h", c_int),
    ("b2", c_int),
    ("b3", c_int),
    ("hr", c_int),
    ("hrslam", c_int),
    ("bb", c_int),
    ("ibb", c_int),
    ("so", c_int),
    ("bf", c_int),
    ("bk", c_int),
    ("wp", c_int),
    ("hb", c_int),
    ("gdp", c_int),
    ("sh", c_int),
    ("sf", c_int),
    ("xi", c_int),
    ("pk", c_int),
    ("w", c_int),
    ("l", c_int),
    ("sv", c_int),
    ("inr", c_int),
    ("inrs", c_int),
    ("xb", c_int),
    ("xbinn", c_int),
    ("gb", c_int),
    ("fb", c_int),
    ("pitches", c_int),
    ("strikes", c_int),
]


CWBoxPitcher._fields_ = [
    ("player_id", c_char_p),
    ("name", c_char_p),
    ("pitching", POINTER(CWBoxPitching)),
    ("prev", POINTER(CWBoxPitcher)),
    ("next", POINTER(CWBoxPitcher)),
]

CWBoxEvent._fields_ = [
    ("players", c_char_p * 20),
    ("inning", c_int),
    ("half_inning", c_int),
    ("runners", c_int),
    ("pickoff", c_int),
    ("outs", c_int),
    ("mark", c_int),
    ("location", c_char * 10),
    ("prev", POINTER(CWBoxEvent)),
    ("next", POINTER(CWBoxEvent)),
]


CWBoxscore._fields_ = [
    ("slots", (POINTER(CWBoxPlayer) * 2) * 10),
    ("pitchers", POINTER(CWBoxPitcher) * 2),
    ("linescore", (c_int * 2) * 50),
    ("score", c_int * 2),
    ("hits", c_int * 2),
    ("errors", c_int * 2),
    ("dp", c_int * 2),
    ("tp", c_int * 2),
    ("lob", c_int * 2),
    ("er", c_int * 2),
    ("risp_ab", c_int * 2),
    ("risp_h", c_int * 2),
    ("outs_at_end", c_int),
    ("walk_off", c_int),
    ("b2_list", "POINTER(CWBoxEvent"),
    ("b3_list", "POINTER(CWBoxEvent"),
    ("hr_list", "POINTER(CWBoxEvent"),
    ("sb_list", "POINTER(CWBoxEvent"),
    ("cs_list", "POINTER(CWBoxEvent"),
    ("po_list", "POINTER(CWBoxEvent"),
    ("sh_list", "POINTER(CWBoxEvent"),
    ("sf_list", "POINTER(CWBoxEvent"),
    ("hp_list", "POINTER(CWBoxEvent"),
    ("ibb_list", "POINTER(CWBoxEvent"),
    ("wp_list", "POINTER(CWBoxEvent"),
    ("bk_list", "POINTER(CWBoxEvent"),
    ("err_list", "POINTER(CWBoxEvent"),
    ("pb_list", "POINTER(CWBoxEvent"),
    ("dp_list", "POINTER(CWBoxEvent"),
    ("tp_list", "POINTER(CWBoxEvent"),
]

