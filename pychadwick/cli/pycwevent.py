import argparse
import os
from io import BytesIO
import tempfile
import zipfile
import requests
import sys
from concurrent.futures import ProcessPoolExecutor
import glob

from pychadwick.chadwick import Chadwick

URL = "https://github.com/chadwickbureau/retrosheet/archive/master.zip"
NUM_CPU = 5
chadwick = Chadwick()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-root",
        required=False,
        help="Location of retrosheet events. "
        "If dir doesn't exist, or if dir is not specified, will download event files",
    )
    parser.add_argument(
        "-n",
        "--num-cpu",
        required=False,
        type=int,
        default=NUM_CPU,
        help="Number of processes to use for parsing",
    )
    return parser.parse_args(sys.argv[1:])


def _download():
    archive = zipfile.ZipFile(BytesIO(requests.get(URL, stream=True).content))
    target = tempfile.gettempdir()
    archive.extractall(path=target)
    return target


def read_from_file_csv(event_file):
    games = chadwick.games(event_file)
    for game in games:
        print(game)
        chadwick.process_game_csv(game)


def main():
    args = _parse_args()
    if not args.data_root:
        data_root = _download()
        events_dir = os.path.join(
            f"{data_root}", "retrosheet-master", "event", "regular"
        )
    else:
        events_dir = args.data_root

    event_files = glob.glob(os.path.join(events_dir, "*EV*"))
    sys.stderr.write(f"stderr: found {len(event_files)} files\n")
    print(",".join(chadwick.active_headers))

    if args.num_cpu == 1:
        _ = list(map(read_from_file_csv, event_files))
    else:
        with ProcessPoolExecutor(args.num_cpu) as mp:
            _ = list(mp.map(read_from_file_csv, event_files))


if __name__ == "__main__":
    main()
