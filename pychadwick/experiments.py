import ctypes
from ctypes import Structure, POINTER, c_char, c_char_p, c_int, pointer

from game import CWGame
from gameiter import CWGameIterator
from roster import CWRoster



def open_and_close(file_name):
    dll = ctypes.cdll.LoadLibrary(
        "/home/bdilday/tmp/chadwick/src/cwtools/.libs/libchadwick2.so"
    )

    fp = open_file(file_name, b"w", dll)
    close_file(fp, dll)

def open_file(file_name, mode, dll):
    fopen = dll.fopen
    fopen.argtypes = ctypes.c_char_p, ctypes.c_char_p,
    fopen.restype = ctypes.c_void_p
    file_ptr = fopen(file_name, mode)
    return file_ptr


def close_file(file_ptr, dll):
    fclose = dll.fclose
    fclose.argtypes = ctypes.c_void_p,
    fclose.restype = ctypes.c_int
    fclose(file_ptr)

def make_game():
    dll = ctypes.cdll.LoadLibrary(
        "/home/bdilday/tmp/chadwick/src/cwtools/.libs/libchadwick2.so"
    )

    cw_game_create = dll.cw_game_create
    cw_game_create.restype = POINTER(CWGame)
    cw_game_create.argtypes = (POINTER(c_char),)
    game_id = ctypes.create_string_buffer(b"ZZZ201908321")
    gp = cw_game_create(game_id)

def main():
#    g = make_game()
    open_and_close(b"testfile.txt")

if __name__ == "__main__":
    main()
