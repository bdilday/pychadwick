import ctypes
import pathlib
import sys

FILE_EXTENSION = {"darwin": "dylib", "linux": "so", "windows": "dll"}


class _ChadwickLibrary:
    library_path = (
        pathlib.Path(__file__).absolute().parent.parent
        / "lib"
        / "cwevent"
        / f"libcwevent.{FILE_EXTENSION.get(sys.platform)}"
    )

    def __init__(self):
        self._dll = None

    @property
    def libchadwick(self):
        if self._dll is None:
            self._dll = ctypes.cdll.LoadLibrary(self.library_path)
        return self._dll
