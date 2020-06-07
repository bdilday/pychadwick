import pytest
from pychadwick.chadwick import Chadwick


@pytest.fixture
def event_path():
    # return (
    #    b"https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/event/regular/1982OAK.EVA"
    # )
    #    return "/tmp/retrosheet-master/event/regular/1982OAK.EVA"
    return "/tmp/retrosheet-master/event/regular/1991BAL.EVA"


def test_chadwick():
    _ = Chadwick()


def test_load_games(event_path):
    chadwick = Chadwick()
    games = chadwick.games(event_path)

    game = next(games)
    game_it = chadwick.process_game(game)
    record = next(game_it)
    assert "GAME_ID" in record.keys()
