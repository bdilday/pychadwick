from ctypes import Structure, c_char, c_int
from enum import IntEnum


class CWEventData(Structure):
    pass


class CEnum(IntEnum):
    @classmethod
    def from_param(cls, self):
        if not isinstance(self, cls):
            raise TypeError
        return self


CWEventType = c_int

"""
https://stackoverflow.com/questions/27199479/using-the-python-enum-module-for-ctypes
"""


class CWEventType_bogus(CEnum):
    CW_EVENT_UNKNOWN = 0
    CW_EVENT_NONE = 1
    CW_EVENT_GENERICOUT = 2
    CW_EVENT_STRIKEOUT = 3
    CW_EVENT_STOLENBASE = 4
    CW_EVENT_INDIFFERENCE = 5
    CW_EVENT_CAUGHTSTEALING = 6
    CW_EVENT_PICKOFFERROR = 7
    CW_EVENT_PICKOFF = 8
    CW_EVENT_WILDPITCH = 9
    CW_EVENT_PASSEDBALL = 10
    CW_EVENT_BALK = 11
    CW_EVENT_OTHERADVANCE = 12
    CW_EVENT_FOULERROR = 13
    CW_EVENT_WALK = 14
    CW_EVENT_INTENTIONALWALK = 15
    CW_EVENT_HITBYPITCH = 16
    CW_EVENT_INTERFERENCE = 17
    CW_EVENT_ERROR = 18
    CW_EVENT_FIELDERSCHOICE = 19
    CW_EVENT_SINGLE = 20
    CW_EVENT_DOUBLE = 21
    CW_EVENT_TRIPLE = 22
    CW_EVENT_HOMERUN = 23
    CW_EVENT_MISSINGPLAY = 24
    CW_EVENT_PITCH_BALL = 100
    CW_EVENT_PITCH_BALL_INTENTIONAL = 101
    CW_EVENT_PITCH_BALL_PITCHOUT = 102
    CW_EVENT_PITCH_BALL_HITBYPITCH = 103
    CW_EVENT_PITCH_BALL_PENALTYBALL = 104
    CW_EVENT_PITCH_INPLAY = 105
    CW_EVENT_PITCH_STRIKE_CALLED = 106
    CW_EVENT_PITCH_STRIKE_SWINGING = 107
    CW_EVENT_PITCH_STRIKE_UNKNOWN = 108
    CW_EVENT_PITCH_STRIKE_FOUL = 109
    CW_EVENT_PITCH_STRIKE_BUNT_MISSED = 110
    CW_EVENT_PITCH_STRIKE_BUNT_FOUL = 111
    CW_EVENT_PITCH_STRIKE_PITCHOUT = 112
    CW_EVENT_PITCH_STRIKE_PITCHOUT_FOUL = 113
    CW_EVENT_PITCH_STRIKE_FOULTIP = 114
    CW_EVENT_PITCH_STRIKE_BUNT_FOULTIP = 115
    CW_EVENT_PITCH_NOPITCH = 116
    CW_EVENT_PITCH_UNKNOWN = 117
    CW_EVENT_PITCH_PICKOFF_PITCHER_FIRST = 118
    CW_EVENT_PITCH_PICKOFF_PITCHER_SECOND = 119
    CW_EVENT_PITCH_PICKOFF_PITCHER_THIRD = 120
    CW_EVENT_PITCH_PICKOFF_CATCHER_FIRST = 121
    CW_EVENT_PITCH_PICKOFF_CATCHER_SECOND = 122
    CW_EVENT_PITCH_PICKOFF_CATCHER_THIRD = 123


CWEventData._fields_ = [
    ("event_type", CWEventType),
    ("advance", c_int * 4),
    ("rbi_flag", c_int * 4),
    ("fc_flag", c_int * 4),
    ("muff_flag", c_int * 4),
    ("play", (c_char * 20) * 4),
    ("sh_flag", c_int),
    ("sf_flag", c_int),
    ("dp_flag", c_int),
    ("gdp_flag", c_int),
    ("tp_flag", c_int),
    ("wp_flag", c_int),
    ("pb_flag", c_int),
    ("foul_flag", c_int),
    ("bunt_flag", c_int),
    ("force_flag", c_int),
    ("sb_flag", c_int * 4),
    ("cs_flag", c_int * 4),
    ("po_flag", c_int * 4),
    ("fielded_by", c_int),
    ("num_putouts", c_int),
    ("num_assists", c_int),
    ("num_errors", c_int),
    ("num_touches", c_int),
    ("putouts", c_int * 3),
    ("assists", c_int * 10),
    ("errors", c_int * 10),
    ("touches", c_int * 20),
    ("error_types", c_char * 10),
    ("batted_ball_type", c_char),
    ("hit_location", c_char * 20),
]
