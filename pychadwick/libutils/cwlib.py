import ctypes
import pathlib


class _ChadwickLibrary:
    library_path = (
        pathlib.Path(__file__).absolute().parent.parent / "lib" / "cwevent" / "libcwevent.so"
    )

    def __init__(self):
        self._dll = None

    @property
    def libchadwick(self):
        if self._dll is None:
            self._dll = ctypes.cdll.LoadLibrary(self.library_path)
        return self._dll

