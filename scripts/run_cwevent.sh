#!/bin/bash

LAST_PWD=$PWD
CWEVENT_EXE=$HOME/github/chadwickbureau/chadwick/src/cwtools/cwevent
FIELDS="0,2,3,4,10,14,34"
SEASON=${1:-"1982"}
TEAM=${2:-"OAK"}
LEAGUE=${3:-"A"}
DATA_ROOT=$HOME/.pybbda/data
OUTPUT_FILE=/tmp/${SEASON}${TEAM}_c_chadwick.csv

cd $DATA_ROOT/retrosheet/retrosheet-master/event/regular/
$CWEVENT_EXE -f $FIELDS -n -y $SEASON ${SEASON}${TEAM}.EV${LEAGUE} > $OUTPUT_FILE
cd $LAST_PWD

echo "output saved to file $OUTPUT_FILE"