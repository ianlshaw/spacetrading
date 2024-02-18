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







The first few turns should look like this:
```
TURN 1-3 EXAMPLE GOES HERE
```

By turn 10 the system should be settled, surveyors on site surveying, miners on site mining or transiting to the MARKETPLACE. Hopefully there's a survey good enough for the COMMAND_SHIP to mine, too. 
```
TURN 10 GOOD SURVEY EXAMPLE GOES HERE
```
Though that's not always the case.
```
TURN 10 BAD SURVEY EXAMPLE GOES HERE
```

Once the system is completely settled, it should look like this:
```
TURN 300 EXAMPLE GOES HERE
```

Happy Space Trading!