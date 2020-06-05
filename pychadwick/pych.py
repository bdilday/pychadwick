import ctypes
from ctypes import (
    POINTER,
    c_char,
    c_char_p,
    c_int,
    pointer,
    create_string_buffer,
)

from pychadwick.game import CWGame
from pychadwick.roster import CWRoster
from pychadwick.league import CWLeague


def read_rosters():
    lib_path = (
        "/home/bdilday/.venvs/pychadwick/lib/python3.7/"
        "site-packages/pychadwick-0.1.0-py3.7-linux-x86_64.egg/"
        "pychadwick/build/cwevent/libcwevent.so"
    )
    dll = ctypes.cdll.LoadLibrary(lib_path)
    filename = b"/home/bdilday/github/chadwickbureau/retrosheet/event/regular/TEAM1961"
    f = dll.cw_league_read_file
    f.argtypes = (POINTER(CWLeague), c_char_p)
    f.restype = c_int
    cw_league_create = dll.cw_league_create
    cw_league_create.argtypes = tuple()
    cw_league_create.restype = POINTER(CWLeague)

    league_p = cw_league_create()

    first_roster = CWRoster(team_id=create_string_buffer(b"jjj", 4))
    last_roster = CWRoster(team_id=create_string_buffer(b"", 4))
    league_p.first_roster = pointer(first_roster)
    league_p.last_roster = pointer(last_roster)

    #    print(league_p.contents.first_roster.contents.team_id.contents.value)
    p = f(league_p, filename)
    print(league_p.contents.first_roster.contents.team_id.contents)
    return p, league_p


def make_game():
    lib_path = (
        "/home/bdilday/.venvs/pychadwick/lib/python3.7/"
        "site-packages/pychadwick-0.1.0-py3.7-linux-x86_64.egg/"
        "pychadwick/build/cwevent/libcwevent.so"
    )
    dll = ctypes.cdll.LoadLibrary(lib_path)

    cw_game_create = dll.cw_game_create
    cw_game_create.restype = POINTER(CWGame)
    cw_game_create.argtypes = (POINTER(c_char),)
    game_id = ctypes.create_string_buffer(b"ZZZ201908321")
    gp = cw_game_create(game_id)
    return gp


def main():
    #    p = read_rosters()
    p = make_game()
    print(p)


if __name__ == "__main__":
    main()
