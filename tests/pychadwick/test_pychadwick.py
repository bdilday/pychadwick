import pytest
from pychadwick.chadwick import Chadwick


@pytest.fixture
def lib_path():
    return (
        "/home/bdilday/.venvs/pychadwick/lib/python3.7/"
        "site-packages/pychadwick-0.1.0-py3.7-linux-x86_64.egg/"
        "pychadwick/build/cwevent/libcwevent.so"
    )


def test_chadwick(lib_path):
    chadwick = Chadwick(lib_path)
