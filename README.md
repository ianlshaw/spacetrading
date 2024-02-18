# spacetrading

This is an automated script used to play the game spacetraders api

REQUIREMENTS:
- python3
- requests library

USAGE:
Modify value of `CALLSIGN` variable in `begin.py` to your desired CALLSIGN.

Run `python3 begin.py`

It will:
  - Purchase a SURVEYOR
  - Purchase a MINING_SHIP
  - Survey, mine and deliver goods required for starter contract

After that it will:
  - Continue surveying, mining and selling goods to the MARKETPLACE indefinitely (until the market collapses)


There are a couple of variables you can modify which can be fun:


The system will purchases ships of the associated type up to these numbers:
```
DESIRED_SURVEYOR_SHIPS = 1
DESIRED_MINING_SHIPS = 1
```

The command ship will only mine if a survey of this quality is found:
```
COMMAND_SHIP_DO_I_MINE_TOLERANCE = 0.5
```

### Explain

The `COMMAND_SHIP`  comes with a `MOUNT_MINING_LASER_II` so we want to use it since it's effectively 2 `EXCAVATORS`.

But it also has a `MOUNT_SURVEYOR_II` which is effectively 2 `SURVEYORS`.

So we want to use both, surveying until we find a deposit with a high enough proportion of `CONTRACT_MINERAL`. Then mine it.

`COMMAND_SHIP_DO_I_MINE_TOLERANCE` defines the proportion of a `deposit` which must be `CONTRACT_MINERAL` for the `COMMAND_SHIP` to mine instead of survey.






Here is an example turn once the system has settled.
This run uses the default values of 
```
DESIRED_SURVEYOR_SHIPS = 1
DESIRED_MINING_SHIPS = 1
COMMAND_SHIP_DO_I_MINE_TOLERANCE = 0.5
```

```
INFO  | TURN 13  START --------------------------
SPACER|-------------------------------------------------------------------
INFO  | SATELLITE | TVRJ-TEST-144-2
INFO  | SATELLITE | TVRJ-TEST-144-2 | LOCATION   | X1-HZ11-H50
INFO  | SATELLITE | TVRJ-TEST-144-2 | STATUS     | DOCKED
INFO  | SATELLITE | TVRJ-TEST-144-2 | FUEL       | 0/0
INFO  | SATELLITE | TVRJ-TEST-144-2 | CARGO      | 0/0
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | SURVEYOR | TVRJ-TEST-144-3
INFO  | SURVEYOR | TVRJ-TEST-144-3 | LOCATION   | X1-HZ11-AD5Z
INFO  | SURVEYOR | TVRJ-TEST-144-3 | STATUS     | IN_ORBIT
INFO  | SURVEYOR | TVRJ-TEST-144-3 | FUEL       | 51/80
INFO  | SURVEYOR | TVRJ-TEST-144-3 | CARGO      | 0/0
INFO  | SURVEY RESULT 0.17 DOES NOT BEAT 0.5
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | COMMAND | TVRJ-TEST-144-1 | ASSIGNMENT | MINING BECAUSE SURVEY GOOD
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | COMMAND | TVRJ-TEST-144-1
INFO  | COMMAND | TVRJ-TEST-144-1 | LOCATION   | X1-HZ11-AD5Z
INFO  | COMMAND | TVRJ-TEST-144-1 | STATUS     | IN_ORBIT
INFO  | COMMAND | TVRJ-TEST-144-1 | FUEL       | 370/400
INFO  | COMMAND | TVRJ-TEST-144-1 | CARGO      | 30/40
INFO  | COMMAND | TVRJ-TEST-144-1 | ASSIGNMENT | MINING
INFO  | COMMAND | TVRJ-TEST-144-1 | SITUATION  | ON SITE AT CONTRACT_ASTEROID_LOCATION
INFO  | COMMAND | TVRJ-TEST-144-1 | MINING     | EXTRACTED 5 IRON_ORE 35/40
SPACER|-------------------------------------------------------------------
INFO  | EXCAVATOR | TVRJ-TEST-144-4 | TRANSIT    | IN_TRANSIT
SPACER|-------------------------------------------------------------------
INFO  | TURN 13  END -----------------------------
SPACER|-------------------------------------------------------------------
INFO  | HTTP COST | 3.0/m
INFO  | CALLSIGN  | TVRJ-TEST-144
INFO  | CREDITS   | 100587
INFO  | SHIPCOUNT | 4
```