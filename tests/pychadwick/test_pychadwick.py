import pytest
from pychadwick.chadwick import Chadwick
import tempfile
import requests

@pytest.fixture
def event_path():
    url = "https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/event/regular/1982OAK.EVA"
    file_path = tempfile.gettempdir() + "/tmp.EVA"
    with open(file_path, "w") as fh:
        fh.write(requests.get(url).text)
    return file_path


def test_chadwick():
    _ = Chadwick()


def test_load_games(event_path):
    chadwick = Chadwick()
    games = chadwick.games(event_path)

    game = next(games)
    game_it = chadwick.process_game(game)
    record = next(game_it)
    assert "GAME_ID" in record.keys()
