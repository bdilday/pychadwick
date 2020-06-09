from pychadwick.chadwick import Chadwick
import tempfile
import requests


def get_event_path(url):
    file_path = tempfile.gettempdir() + "/tmp.EVA"
    with open(file_path, "w") as fh:
        fh.write(requests.get(url).text)
    return file_path


def test_chadwick():
    _ = Chadwick()


def test_load_games():
    chadwick = Chadwick()

    for team_event in ["1982OAK.EVA", "1991BAL.EVA", "1954PHI.EVN"]:
        event_path = get_event_path(
            f"https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/event/regular/{team_event}"
        )
        games = chadwick.games(event_path)
        game = next(games)
        game_it = chadwick.process_game(game)
        record = next(game_it)
        assert "GAME_ID" in record.keys()


def test_load_games_to_df():
    chadwick = Chadwick()

    for team_event in ["1982OAK.EVA", "1991BAL.EVA", "1954PHI.EVN"]:
        event_path = get_event_path(
            f"https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/event/regular/{team_event}"
        )
        games = chadwick.games(event_path)
        dfs = [chadwick.game_to_dataframe(game) for game in games]

