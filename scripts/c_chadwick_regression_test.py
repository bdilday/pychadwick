import os
import pathlib
import subprocess
import sys

import pandas as pd
from pandas.testing import assert_frame_equal
from pychadwick.chadwick import Chadwick
from pybbda import PYBBDA_DATA_ROOT

CHADWICK_SCRIPT = str(pathlib.Path(__file__).absolute().parent / "run_cwevent.sh")


def get_cchadwick_df():
    return pd.read_csv(LOCAL_EVENT_FILE)


def get_pychadwick_df():
    event_file = os.path.join(
        PYBBDA_DATA_ROOT,
        "retrosheet",
        "retrosheet-master",
        "event",
        "regular",
        f"{args.season}{args.team}.EV{args.league}",
    )
    pychadwick_df = chadwick.event_file_to_dataframe(event_file)
    return pychadwick_df


def check_equality(pychadwick_df, cchadwick_df):
    game_ids = pychadwick_df.GAME_ID.unique()
    num_errors = 0
    for game_id in game_ids:
        df1 = pychadwick_df.query('GAME_ID == "{}"'.format(game_id))
        df2 = cchadwick_df.query('GAME_ID == "{}"'.format(game_id))
        try:
            assert_frame_equal(df1, df2, check_dtype=False)
        except AssertionError:
            print(f"error: game {game_id} is not identical")
            num_errors += 1
    return num_errors


def main():
    pychadwick_df = get_pychadwick_df()
    cchadwick_df = get_cchadwick_df()

    num_errors = check_equality(pychadwick_df, cchadwick_df)
    sys.exit(int(bool(num_errors)))

import argparse
def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", required=False, default=1982, type=int)
    parser.add_argument("--team", required=False, default="OAK")
    parser.add_argument("--league", required=False, default="A")
    return parser.parse_args(sys.argv[1:])

if __name__ == "__main__":
    args = _parse_args()
    LOCAL_EVENT_FILE = f"/tmp/{args.season}{args.team}_c_chadwick.csv"
    #if not os.path.exists(LOCAL_EVENT_FILE):
    subprocess.run([CHADWICK_SCRIPT, str(args.season), args.team, args.league])

    chadwick = Chadwick()
    for h in chadwick.all_headers:
        chadwick.unset_event_field(h)
    headers = [
        "GAME_ID",
        "INN_CT",
        "OUTS_CT",
        "BAT_ID",
        "PIT_ID",
        "EVENT_CD",
        "BAT_HOME_ID",
    ]
    for h in headers:
        chadwick.set_event_field(h)
    main()
