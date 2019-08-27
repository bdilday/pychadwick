import ctypes
from ctypes import Structure, POINTER, c_char, c_char_p, c_int, pointer, create_string_buffer

from game import CWGame
from gameiter import CWGameIterator
from roster import CWRoster
from league import CWLeague

def read_rosters():
    dll = ctypes.cdll.LoadLibrary("/home/bdilday/tmp/chadwick/src/cwtools/.libs/libchadwick2.so")                                                   
    filename = b"/home/bdilday/github/chadwickbureau/retrosheet/event/regular/TEAM1961"                                                             
    f = dll.cw_league_read_file
    f.argtypes = (POINTER(CWLeague), c_char_p,)
    f.restype = c_int
    first_roster = CWRoster(team_id=create_string_buffer(b"", 4))
    last_roster = CWRoster(team_id=create_string_buffer(b"", 4))
    league_p = pointer(CWLeague(first_roster = pointer(first_roster), last_roster=pointer(last_roster)))
    
    p = f(league_p, filename)
    return p, league_p


def make_game():
    dll = ctypes.cdll.LoadLibrary(
        "/home/bdilday/tmp/chadwick/src/cwtools/.libs/libchadwick2.so"
    )

    cw_game_create = dll.cw_game_create
    cw_game_create.restype = POINTER(CWGame)
    cw_game_create.argtypes = (POINTER(c_char),)
    game_id = ctypes.create_string_buffer(b"ZZZ201908321")
    gp = cw_game_create(game_id)
    return gp

def main():
    p = read_rosters()
    print(p)

if __name__ == "__main__":
    main()
