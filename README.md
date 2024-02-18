# spacetrading

This is an automated script used to play the game spacetraders api

### REQUIREMENTS:
- python3
- requests library

### USAGE:  
- Modify value of `CALLSIGN` in: `begin.py` to your desired `CALLSIGN`.
- Run `python3 begin.py`

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

The `COMMAND_SHIP` ship will only mine if a survey of this quality is found:
```
COMMAND_SHIP_DO_I_MINE_TOLERANCE = 0.5
```

### Explain

The `COMMAND_SHIP`  comes with a `MOUNT_MINING_LASER_II` so we want to use it since it's effectively 2 `EXCAVATORS`.

But it also has a `MOUNT_SURVEYOR_II` which is effectively 2 `SURVEYORS`.

So we want to use both, surveying until we find a deposit with a high enough proportion of `CONTRACT_MINERAL`. Then mine it.

`COMMAND_SHIP_DO_I_MINE_TOLERANCE` defines the proportion of a survey's `deposit` which must be `CONTRACT_MINERAL` for the `COMMAND_SHIP` to mine instead of survey.







The first turn will be a little different to susequent ones.  
It should look like this:
```
PS F:\repos\spacetrading> python .\begin.py
INFO  | AUTH FILE ABSENT
INFO  | INITIATE INITIAL INITIALIZATION
INFO  | WROTE NEW AUTH FILE
SPACER|-------------------------------------------------------------------
INFO  | TURN 1  START --------------------------
SPACER|-------------------------------------------------------------------
INFO  | SATELLITE | TVRJ-TEST-145-2
INFO  | SATELLITE | TVRJ-TEST-145-2 | LOCATION   | X1-QF3-H56
INFO  | SATELLITE | TVRJ-TEST-145-2 | STATUS     | DOCKED    
INFO  | SATELLITE | TVRJ-TEST-145-2 | FUEL       | 0/0       
INFO  | SATELLITE | TVRJ-TEST-145-2 | CARGO      | 0/0       
INFO  | SATELLITE | TVRJ-TEST-145-2 | TRANSIT    | DOCKED    
INFO  | PURCHASED SHIP_SURVEYOR at X1-QF3-H56
INFO  | PURCHASED SURVEYOR
INFO  | SATELLITE | TVRJ-TEST-145-2 | TRANSIT    | DOCKED
INFO  | PURCHASED SHIP_MINING_DRONE at X1-QF3-H56
INFO  | PURCHASED MINER
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | SURVEYOR | TVRJ-TEST-145-3
INFO  | SURVEYOR | TVRJ-TEST-145-3 | LOCATION   | X1-QF3-H56
INFO  | SURVEYOR | TVRJ-TEST-145-3 | STATUS     | DOCKED
INFO  | SURVEYOR | TVRJ-TEST-145-3 | FUEL       | 80/80
INFO  | SURVEYOR | TVRJ-TEST-145-3 | CARGO      | 0/0
INFO  | SURVEYOR | TVRJ-TEST-145-3 | TRANSIT    | IN_ORBIT
INFO  | SURVEYOR | TVRJ-TEST-145-3 | TRANSIT    | X1-QF3-H56 TO X1-QF3-AD5C
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | COMMAND | TVRJ-TEST-145-1 | ASSIGNMENT | SURVEYING BECAUSE SURVEY BAD
SPACER|-------------------------------------------------------------------   
SPACER|-------------------------------------------------------------------   
INFO  | COMMAND | TVRJ-TEST-145-1
INFO  | COMMAND | TVRJ-TEST-145-1 | LOCATION   | X1-QF3-A1
INFO  | COMMAND | TVRJ-TEST-145-1 | STATUS     | DOCKED
INFO  | COMMAND | TVRJ-TEST-145-1 | FUEL       | 400/400
INFO  | COMMAND | TVRJ-TEST-145-1 | CARGO      | 0/40
INFO  | COMMAND | TVRJ-TEST-145-1 | TRANSIT    | IN_ORBIT
INFO  | COMMAND | TVRJ-TEST-145-1 | TRANSIT    | X1-QF3-A1 TO X1-QF3-AD5C
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | EXCAVATOR | TVRJ-TEST-145-4
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | LOCATION   | X1-QF3-H56
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | STATUS     | DOCKED
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | FUEL       | 80/80
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | CARGO      | 0/15
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | ASSIGNMENT | MINING
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | TRANSIT    | IN_ORBIT
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | TRANSIT    | X1-QF3-H56 TO X1-QF3-AD5C
SPACER|-------------------------------------------------------------------
INFO  | TURN 1  END -----------------------------
SPACER|-------------------------------------------------------------------
INFO  | HTTP COST | 6.0/m
INFO  | CALLSIGN  | TVRJ-TEST-145
INFO  | CREDITS   | 93120
INFO  | SHIPCOUNT | 4
SPACER|-------------------------------------------------------------------
```

By TURN 10 the system should be settled, `SURVEYOR_SHIPS` on site surveying, `MINING_SHIPS` on site mining or transiting to the `MARKETPLACE`.  
Hopefully there's a survey good enough for the `COMMAND_SHIP` to mine, too. 
```
INFO  | TURN 10  START --------------------------
SPACER|-------------------------------------------------------------------
INFO  | SATELLITE | TVRJ-TEST-145-2
INFO  | SATELLITE | TVRJ-TEST-145-2 | LOCATION   | X1-QF3-H56
INFO  | SATELLITE | TVRJ-TEST-145-2 | STATUS     | DOCKED
INFO  | SATELLITE | TVRJ-TEST-145-2 | FUEL       | 0/0
INFO  | SATELLITE | TVRJ-TEST-145-2 | CARGO      | 0/0
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | SURVEYOR | TVRJ-TEST-145-3
INFO  | SURVEYOR | TVRJ-TEST-145-3 | LOCATION   | X1-QF3-AD5C
INFO  | SURVEYOR | TVRJ-TEST-145-3 | STATUS     | IN_ORBIT
INFO  | SURVEYOR | TVRJ-TEST-145-3 | FUEL       | 61/80
INFO  | SURVEYOR | TVRJ-TEST-145-3 | CARGO      | 0/0
INFO  | SURVEY RESULT 0.33 DOES NOT BEAT 0.67
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | COMMAND | TVRJ-TEST-145-1 | ASSIGNMENT | MINING BECAUSE SURVEY GOOD
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | COMMAND | TVRJ-TEST-145-1
INFO  | COMMAND | TVRJ-TEST-145-1 | LOCATION   | X1-QF3-AD5C
INFO  | COMMAND | TVRJ-TEST-145-1 | STATUS     | IN_ORBIT
INFO  | COMMAND | TVRJ-TEST-145-1 | FUEL       | 376/400
INFO  | COMMAND | TVRJ-TEST-145-1 | CARGO      | 33/40
INFO  | COMMAND | TVRJ-TEST-145-1 | ASSIGNMENT | MINING
INFO  | COMMAND | TVRJ-TEST-145-1 | SITUATION  | ON SITE AT CONTRACT_ASTEROID_LOCATION
INFO  | COMMAND | TVRJ-TEST-145-1 | MINING     | EXTRACTED 5 IRON_ORE 38/40
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | EXCAVATOR | TVRJ-TEST-145-4
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | LOCATION   | X1-QF3-H55
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | STATUS     | IN_ORBIT
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | FUEL       | 42/80
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | CARGO      | 15/15
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | ASSIGNMENT | MINING
INFO  | EXCAVATOR | TVRJ-TEST-145-4 IS ALREADY AT CONTRACT_DELIVERY_LOCATION
INFO  | EXCAVATOR | TVRJ-TEST-145-4 DOCKING
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | TRANSIT    | DOCKED AT X1-QF3-H55
INFO  | TVRJ-TEST-145-4 | SOLD       | 8 COPPER_ORE for 576
INFO  | TVRJ-TEST-145-4 | SOLD       | 7 IRON_ORE for 483
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | TRANSIT    | IN_ORBIT
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | TRANSIT    | X1-QF3-H55 TO X1-QF3-AD5C
SPACER|-------------------------------------------------------------------
INFO  | TURN 10  END -----------------------------
SPACER|-------------------------------------------------------------------
INFO  | HTTP COST | 6.0/m
INFO  | CALLSIGN  | TVRJ-TEST-145
INFO  | CREDITS   | 94179
INFO  | SHIPCOUNT | 4
SPACER|-------------------------------------------------------------------
```
Though that's not always the case.
```
TURN 10 BAD SURVEY EXAMPLE GOES HERE
```

If you just leave it for a while, it should look like this:
```
INFO  | TURN 356  START --------------------------
SPACER|-------------------------------------------------------------------
INFO  | SATELLITE | TVRJ-TEST-145-2
INFO  | SATELLITE | TVRJ-TEST-145-2 | LOCATION   | X1-QF3-H56
INFO  | SATELLITE | TVRJ-TEST-145-2 | STATUS     | DOCKED
INFO  | SATELLITE | TVRJ-TEST-145-2 | FUEL       | 0/0
INFO  | SATELLITE | TVRJ-TEST-145-2 | CARGO      | 0/0
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | SURVEYOR | TVRJ-TEST-145-3
INFO  | SURVEYOR | TVRJ-TEST-145-3 | LOCATION   | X1-QF3-AD5C
INFO  | SURVEYOR | TVRJ-TEST-145-3 | STATUS     | IN_ORBIT
INFO  | SURVEYOR | TVRJ-TEST-145-3 | FUEL       | 61/80
INFO  | SURVEYOR | TVRJ-TEST-145-3 | CARGO      | 0/0
INFO  | SURVEY RESULT 0.0 DOES NOT BEAT 1.0
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | COMMAND | TVRJ-TEST-145-1 | ASSIGNMENT | MINING BECAUSE SURVEY GOOD
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | COMMAND | TVRJ-TEST-145-1
INFO  | COMMAND | TVRJ-TEST-145-1 | LOCATION   | X1-QF3-AD5C
INFO  | COMMAND | TVRJ-TEST-145-1 | STATUS     | IN_ORBIT
INFO  | COMMAND | TVRJ-TEST-145-1 | FUEL       | 381/400
INFO  | COMMAND | TVRJ-TEST-145-1 | CARGO      | 36/40
INFO  | COMMAND | TVRJ-TEST-145-1 | ASSIGNMENT | MINING
INFO  | COMMAND | TVRJ-TEST-145-1 | SITUATION  | ON SITE AT CONTRACT_ASTEROID_LOCATION
INFO  | COMMAND | TVRJ-TEST-145-1 | MINING     | EXTRACTED 4 IRON_ORE 40/40
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
SPACER|-------------------------------------------------------------------
INFO  | EXCAVATOR | TVRJ-TEST-145-4
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | LOCATION   | X1-QF3-AD5C
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | STATUS     | IN_ORBIT
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | FUEL       | 61/80
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | CARGO      | 6/15
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | ASSIGNMENT | MINING
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | SITUATION  | ON SITE AT CONTRACT_ASTEROID_LOCATION       
INFO  | EXCAVATOR | TVRJ-TEST-145-4 | MINING     | EXTRACTED 1 IRON_ORE 7/15
SPACER|-------------------------------------------------------------------
INFO  | TURN 356  END -----------------------------
SPACER|-------------------------------------------------------------------
INFO  | HTTP COST | 3.5/m
INFO  | CALLSIGN  | TVRJ-TEST-145
INFO  | CREDITS   | 162709
INFO  | SHIPCOUNT | 4
SPACER|-------------------------------------------------------------------
```

Happy Space Trading!