# pychadwick

A Python package to interface with the `Chadwick` libray.  
`Chadwick` is a set of tools for parsing retrosheet data
and is available at 

http://chadwick.sourceforge.net/doc/index.html

https://github.com/chadwickbureau/chadwick

## Features

As of now this package supports retrosheet event data only.

## Installation

```bash
$ pip install pychadwick
```

## Example use

#### Load events

Load events for a game from a file stored on the web

```python

>>> from pychadwick.chadwick import Chadwick                                                                                    

>>> chadwick = Chadwick()                                                                                                       

>>> file_path = "https://raw.githubusercontent.com/chadwickbureau/retrosheet/master/event/regular/1982OAK.EVA" 

>>> games = chadwick.games(file_path)                                                                                           

>>> game = next(games)                                                                                                          

>>> df = chadwick.game_to_dataframe(game)                                                                                       

>>> df                                                                                                                           
         GAME_ID AWAY_TEAM_ID  INN_CT  BAT_HOME_ID  ...  ASS9_FLD_CD  ASS10_FLD_CD  UNKNOWN_OUT_EXC_FL UNCERTAIN_PLAY_EXC_FL
0   OAK198204060          CAL       1            0  ...            0             0                   F                     F
1   OAK198204060          CAL       1            0  ...            0             0                   F                     F
2   OAK198204060          CAL       1            0  ...            0             0                   F                     F
3   OAK198204060          CAL       1            1  ...            0             0                   F                     F
4   OAK198204060          CAL       1            1  ...            0             0                   F                     F
..           ...          ...     ...          ...  ...          ...           ...                 ...                   ...
81  OAK198204060          CAL      11            1  ...            0             0                   F                     F
82  OAK198204060          CAL      11            1  ...            0             0                   F                     F
83  OAK198204060          CAL      11            1  ...            0             0                   F                     F
84  OAK198204060          CAL      11            1  ...            0             0                   F                     F
85  OAK198204060          CAL      11            1  ...            0             0                   F                     F

[86 rows x 159 columns]
```

Load events for a game from a local file

```python

>>> file_path = " /tmp/retrosheet-master/event/regular/1982OAK.EVA"

>>> games = chadwick.games(file_path)                                                                                           

>>> game = next(games)                                                                                                          

>>> df = chadwick.game_to_dataframe(game)                                                                                       

>>> df                                                                                                                           
         GAME_ID AWAY_TEAM_ID  INN_CT  BAT_HOME_ID  ...  ASS9_FLD_CD  ASS10_FLD_CD  UNKNOWN_OUT_EXC_FL UNCERTAIN_PLAY_EXC_FL
0   OAK198204060          CAL       1            0  ...            0             0                   F                     F
1   OAK198204060          CAL       1            0  ...            0             0                   F                     F
2   OAK198204060          CAL       1            0  ...            0             0                   F                     F
3   OAK198204060          CAL       1            1  ...            0             0                   F                     F
4   OAK198204060          CAL       1            1  ...            0             0                   F                     F
..           ...          ...     ...          ...  ...          ...           ...                 ...                   ...
81  OAK198204060          CAL      11            1  ...            0             0                   F                     F
82  OAK198204060          CAL      11            1  ...            0             0                   F                     F
83  OAK198204060          CAL      11            1  ...            0             0                   F                     F
84  OAK198204060          CAL      11            1  ...            0             0                   F                     F
85  OAK198204060          CAL      11            1  ...            0             0                   F                     F

[86 rows x 159 columns]
```

Check which columns are defined

```python
>>>  chadwick.all_headers
```

Check which columns are enabled

```python
>>>  chadwick.active_headers
```

Disable all columns, and add only `GAME_ID` and `BAT_ID`

```python
>>> _ = [chadwick.unset_event_field(e) for e in chadwick.all_headers]                                                          

>>> chadwick.active_headers                                                                                                    
[]

>>> chadwick.set_event_field("GAME_ID")                                                                                        

>>> chadwick.set_event_field("BAT_ID")                                                                                         

>>> games = chadwick.games(file_path)                                                                                          

>>>  game = next(games)                                                                                                         

>>> df = chadwick.game_to_dataframe(game)                                                                                      

>>> df

         GAME_ID    BAT_ID
0   OAK198204060  burlr001
1   OAK198204060  lynnf001
2   OAK198204060  carer001
3   OAK198204060  hendr001
4   OAK198204060  murpd002
..           ...       ...
81  OAK198204060  meyed001
82  OAK198204060  armat001
83  OAK198204060  grosw001
84  OAK198204060  spenj101
85  OAK198204060  loped001

[86 rows x 2 columns]
```

Activate all the columns again

```python
>>> chadwick.set_all_headers()
```
