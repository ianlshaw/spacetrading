import requests
import json
import time
import io
from datetime import datetime,timedelta  


COMMAND_SHIP_DO_I_MINE_TOLERANCE = 0.5
REFUEL_PERCENT_THRESHOLD = 50
SURVEY_AGE_TOLERANCE = timedelta(minutes=3)
TURN_TIMER = 120

INFO_STRING  = 'INFO  |'
WARN_STRING  = 'WARN  |'
ERROR_STRING = 'ERROR |'

SYSTEM_STRING     = 'SYSTEM'
TURN_STRING       = '|============|'
MINING_STRING     = '| MINING     |'
ASSIGNMENT_STRING = '| ASSIGNMENT |'

TRANSIT_STRING    = '| TRANSIT    |'
FUEL_STRING       = '| FUEL       |'
SURVEY_STRING     = '| SURVEY     |'
COOLDOWN_STRING   = '| COOLDOWN   |'
CARGO_STRING      = '| CARGO      |'
SOLD_STRING       = '| SOLD       |'



CONTENT_TYPE = 'application/json'
BASE_URL = 'https://api.spacetraders.io/v2'

mining_ships = ['TVRJ-3']
COMMAND_SHIP = 'TVRJ-1'
PROBE_SHIP = 'TVRJ-2'
system = 'X1-KK49'
SURVEY_SHIP = 'TVRJ-4'

authorization_token_file_path = 'auth_token.txt'
authorization_token_file_descriptor = io.open(authorization_token_file_path, 'r', newline='' )
AUTHORIZATION_TOKEN = authorization_token_file_descriptor.read().rstrip()

DEFAULT_HEADERS = {'Content-Type': f"{CONTENT_TYPE}", 'Authorization': f"Bearer {AUTHORIZATION_TOKEN}" }
APPLICATION_HEADER = {'Content-Type': f"{CONTENT_TYPE}" }

# These should be populated once on begin by contract()
CONTRACT_DELIVERY_LOCATION = 'X1-KK49-H56'
CONTRACT_ASTEROID_LOCATION = 'X1-KK49-BD5X'
CONTRACT_ID = 'clshregbn001ks60cje4upb6g'
CONTRACT_MINERAL = 'ALUMINUM_ORE'
BEST_SURVEY = ''
BEST_SURVEY_SCORE = 0.00

# This is user discretion. What are you looking for?
GARBAGE = ['QUARTZ_SAND', 'ICE_WATER', 'SILICON_CRYSTALS']
SALE_GOODS = ['COPPER_ORE', 'IRON_ORE', 'ALUMINUM_ORE']


def prettyprint(blob):
  json_object = json.loads(blob)
  json_formatted_str = json.dumps(json_object, indent=2)
  print(json_formatted_str)

def get_status():
  r = requests.get(f'{BASE_URL}', headers=DEFAULT_HEADERS)
  json_object = json.loads(r.text)
  status = json_object['status']
  leaderboards = json_object['leaderboards']
  richest_agent_in_the_galaxy = leaderboards['mostCredits'][0]
  second_richest_agent_in_the_galaxy = leaderboards['mostCredits'][1]
  third_richest_agent_in_the_galaxy = leaderboards['mostCredits'][2]
  print(status)
  print(' ')
  print('1.')
  print(richest_agent_in_the_galaxy['agentSymbol'])
  print(richest_agent_in_the_galaxy['credits'])
  print(' ')
  print('2.')
  print(second_richest_agent_in_the_galaxy['agentSymbol'])
  print(second_richest_agent_in_the_galaxy['credits'])
  print(' ')
  print('3.')
  print(third_richest_agent_in_the_galaxy['agentSymbol'])
  print(third_richest_agent_in_the_galaxy['credits'])

def create_agent():
  payload = {"symbol": "TVRJ", "faction": "COSMIC" }
  r = requests.post(f'{BASE_URL}/register', json=payload, headers=APPLICATION_HEADER)
  print(r.text)


  if r.status_code != 200:
    json_object = r.json()
    print(json_object['error']['message'])

def my_agent():
  r = requests.get(f'{BASE_URL}/my/agent', headers=DEFAULT_HEADERS)
 # prettyprint(r.text)
  json_object = json.loads(r.text)
  symbol = json_object['data']['symbol']
  credits = json_object['data']['credits']
  shipCount = json_object['data']['shipCount']
  print(f'Welcome back, {symbol}')
  print('')
  print('Balance:')
  print(credits)
  print()
  print('shipCount')
  print(shipCount)
  

def waypoint(systemSymbol, waypointSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints/{waypointSymbol}', headers=DEFAULT_HEADERS)
  prettyprint(r.text)

def contract():
  r = requests.get(f'{BASE_URL}/my/contracts', headers=DEFAULT_HEADERS) 
  json_object = r.json()
  contract_id = json_object['data'][0]['id']
  print(r.text)
  print(contract_id)
  return(contract_id)

def accept_contract(contract_id):
  r = requests.post(f'{BASE_URL}/my/contracts/{contract_id}/accept', headers=DEFAULT_HEADERS) 
  prettyprint(r.text)

def find_a_shipyard(systemSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints?traits=SHIPYARD', headers=DEFAULT_HEADERS)
  json_object = json.loads(r.text)
  data = json_object['data']

  for item in data:
    print(item["symbol"], item["type"])

def find_a_market(systemSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints?traits=MARKETPLACE', headers=DEFAULT_HEADERS)
  json_object = json.loads(r.text)
  data = json_object['data']

  #prettyprint(r.text)
  for item in data:
    symbol = item["symbol"]
    print(symbol)
    view_market_data(systemSymbol, symbol)
    print(' ')

def find_market_for_cargo(systemSymbol, miningShipSymbol):
  print('1')

def view_available_ships(systemSymbol, shipyardWaypointSymbol):
    r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints/{shipyardWaypointSymbol}/shipyard',  headers=DEFAULT_HEADERS)
    prettyprint(r.text)

def buy_ship(shipType, shipyardWaypointSymbol):
  payload = {'shipType': f"{shipType}", 'waypointSymbol': f"{shipyardWaypointSymbol}" }
  r = requests.post(f'{BASE_URL}/my/ships', json=payload, headers=DEFAULT_HEADERS) 
  prettyprint(r.text)

def my_ships():
    r = requests.get(f'{BASE_URL}/my/ships',  headers=DEFAULT_HEADERS)
    prettyprint(r.text)

def get_ship(shipSymbol):
    r = requests.get(f'{BASE_URL}/my/ships/{shipSymbol}',  headers=DEFAULT_HEADERS)
    #prettyprint(r.text)
    return r.text

def find_nearby_asteroid(systemSymbol):
    r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints?type=ENGINEERED_ASTEROID',  headers=DEFAULT_HEADERS)
    json_object = json.loads(r.text)
    data = json_object['data']

    for item in data:
      print(item["symbol"])

def my_ships():
    r = requests.get(f'{BASE_URL}/my/ships', headers=DEFAULT_HEADERS)
    json_object = json.loads(r.text)
    data = json_object['data']

    for item in data:
      print(item["symbol"])

def orbit(get_ship_json):
  shipSymbol = get_ship_json['data']['symbol']
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/orbit', headers=DEFAULT_HEADERS)
  json_object = r.json()
  if r.status_code != 200:
    print(json_object['error']['message'])
    return
  status = json_object['data']['nav']['status']
  nav = json_object['data']['nav']
  print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} {status}')

def move(get_ship_json, waypointSymbol):
  shipSymbol = get_ship_json['data']['symbol']
  payload = {'waypointSymbol': f"{waypointSymbol}" }
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/navigate', json=payload, headers=DEFAULT_HEADERS) 
  json_object = r.json()

  if r.status_code != 200:
    print(json_object['error']['message'])
    return

  destination_symbol = json_object['data']['nav']['route']['destination']['symbol']
  departure_symbol = json_object['data']['nav']['route']['departure']['symbol']
    
  print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} {departure_symbol} TO {destination_symbol}')

def dock(get_ship_json):
  shipSymbol = get_ship_json['data']['symbol']
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/dock', headers=DEFAULT_HEADERS) 
  json_object = json.loads(r.text)

  if r.status_code != 200:
    print(json_object['error']['message'])
    return
  destination = json_object['data']['nav']['route']['destination']['symbol']
  status = json_object['data']['nav']['status']
  
  print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} {status} AT {destination}')

def fuel_tank_free_space(get_ship_json):
  shipSymbol = get_ship_json['data']['symbol']
  fuel = get_ship_json['data']['fuel']

def refuel(get_ship_json):
    shipSymbol = get_ship_json['data']['symbol']
    print(f'{INFO_STRING} {shipSymbol} {FUEL_STRING} REFUELLING')
    r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/refuel', headers=DEFAULT_HEADERS) 
    json_object = r.json()
    if r.status_code != 200:
      print(json_object['error']['message'])
    else:
      data = json_object['data']
      totalPrice = json_object['data']['transaction']['totalPrice']
      units = json_object['data']['transaction']['units']
      print(f'{INFO_STRING} {shipSymbol} {FUEL_STRING} REFUELLED AND PAID {totalPrice} FOR {units} OF FUEL')

def extract(miningShipSymbol):
    print(f'{miningShipSymbol} Extracting...')
    r = requests.post(f'{BASE_URL}/my/ships/{miningShipSymbol}/extract', headers=DEFAULT_HEADERS) 
    json_object = r.json()
    if r.status_code != 201:
      print(json_object['error']['message'])
    else:
      data = json_object['data']
      extraction = data['extraction']
      haul = extraction['yield']
      mined_symbol = haul['symbol']
      units = haul['units']

      
      max_capacity = data['cargo']['capacity']
      capacity = data['cargo']['units']
      print(f'{miningShipSymbol} {MINING_STRING} EXTRACTED {units} {mined_symbol} AND IS {capacity}/{max_capacity}')
      
def view_market_data(systemSymbol, waypointSymbol):
    r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints/{waypointSymbol}/market', headers=DEFAULT_HEADERS)
 
    json_object = json.loads(r.text)

    # ['data']['tradeGoods'] likely only exists if you have a ship at the waypoint.

    data = json_object['data']['imports']
    for item in data:
      print(f'{item["symbol"]}')
     # print(f'volume {item["tradeVolume"]}')
     # print(f'supply {item["supply"]}')
     # print(f'buy@  {item["purchasePrice"]}')
     # print(f'sell@ {item["sellPrice"]}')

      
def sell(get_ship_json, goodsSymbol, units):
    shipSymbol = get_ship_json['data']['symbol']
    payload = {'symbol': f"{goodsSymbol}", 'units': f"{units}" }
    r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/sell', json=payload, headers=DEFAULT_HEADERS) 
    json_object = json.loads(r.text)
    if r.status_code != 201:
      error = json_object['error']
      message = error['message']
      return
    
    totalPrice = json_object['data']['transaction']['totalPrice']
    

    print(f'{INFO_STRING} {shipSymbol} {SOLD_STRING} {units} {goodsSymbol} for {totalPrice}')
    

def deliver_goods(miningShipSymbol, tradeSymbol, units, contractId):
    payload = {'shipSymbol': f"{miningShipSymbol}", 'tradeSymbol': f"{tradeSymbol}", 'units': f"{units}" }
    r = requests.post(f'{BASE_URL}/my/contracts/{contractId}/deliver', json=payload, headers=DEFAULT_HEADERS) 
    prettyprint(r.text)

def fulfil_contract(contractId):
    r = requests.post(f'{BASE_URL}/my/contracts/{contractId}/fulfill', headers=DEFAULT_HEADERS) 
    prettyprint(r.text)

def jettison_cargo(get_ship_json, cargoSymbol, units):
  shipSymbol = get_ship_json['data']['symbol']
  payload = {'shipSymbol': f"{shipSymbol}", 'symbol': f"{cargoSymbol}", 'units': f"{units}" }
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/jettison', json=payload, headers=DEFAULT_HEADERS) 
  json_object = r.json()
  if r.status_code != 200:
    error = json_object['error']
    message = error['message']
  max_capacity = get_ship_json['data']['cargo']['capacity']
  capacity = get_ship_json['data']['cargo']['units']
  print(f'{INFO_STRING} {shipSymbol} {MINING_STRING} JETTISONED {units} {cargoSymbol} {capacity}/{max_capacity}')

def is_best_survey_expired():
  print(f'{INFO_STRING} {SYSTEM_STRING} {SURVEY_STRING} CHECKING EXPIRATION')
  if BEST_SURVEY_SCORE == 0.00:
    print(f'{WARN_STRING} {SYSTEM_STRING} {SURVEY_STRING} NOT FOUND')
    return False

  time_now = datetime.now().isoformat()
  time_now_string = f"{time_now}Z"
  time_now_dt = datetime.strptime(time_now_string, "%Y-%m-%dT%H:%M:%S.%fZ")
  expiration = BEST_SURVEY['expiration']
  expiration_dt = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S.%fZ")
  remaining_time_dt = expiration_dt - time_now_dt 

  print(f'{INFO_STRING} {SYSTEM_STRING} {SURVEY_STRING} {remaining_time_dt} REMAINING')

  if remaining_time_dt < SURVEY_AGE_TOLERANCE:
    #print(f'{WARN_STRING} {SYSTEM_STRING} {SURVEY_STRING} EXPIRES SOON')
    purge_expired_survey()
    return True
  else:
    #print(f'{INFO_STRING} {SYSTEM_STRING} {SURVEY_STRING} EXPIRATION WITHIN SURVEY_AGE_TOLERANCE')
    return False

def purge_expired_survey():
  global BEST_SURVEY
  global BEST_SURVEY_SCORE
  BEST_SURVEY = ''
  BEST_SURVEY_SCORE = 0.00
  print(f'{INFO_STRING} {SYSTEM_STRING} {SURVEY_STRING} PURGED BECAUSE EXPIRING')


def perform_survey(shipSymbol):
  #print(f'{INFO_STRING} {shipSymbol} perform_survey')
  if is_best_survey_expired():
    purge_expired_survey
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/survey', headers=DEFAULT_HEADERS) 
  json_object = r.json()


  if r.status_code == 201:
     
    return json_object
  else:
    print(json_object['error']['message'])



def extract_resources_with_survey(get_ship_json, survey):
  shipSymbol = get_ship_json['data']['symbol']
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/extract/survey', json=survey, headers=DEFAULT_HEADERS) 
  json_object = r.json()
  if r.status_code != 201:
    print(json_object['error']['message'])
  else:
    data = json_object['data']
    extraction = data['extraction']
    haul = extraction['yield']
    mined_symbol = haul['symbol']
    units = haul['units']
    max_capacity = data['cargo']['capacity']
    capacity = data['cargo']['units']
    print(f'{INFO_STRING} {shipSymbol} {MINING_STRING} EXTRACTED {units} {mined_symbol} {capacity}/{max_capacity}')
    for garbageSymbol in GARBAGE:
      if mined_symbol == garbageSymbol:
        jettison_cargo(get_ship_json, mined_symbol, units)

    
    



def how_much_of_x_does_ship_have_in_cargo(get_ship_json, cargoSymbol):
  
  shipSymbol = get_ship_json['data']['symbol']
  inventory = get_ship_json['data']['cargo']['inventory']
  for item in inventory:
    if item['symbol'] == cargoSymbol:
      return item['units']
  return 0

def dump_garbage(get_ship_json):
  
  shipSymbol = get_ship_json['data']['symbol']
  for cargoSymbol in GARBAGE:
    units = how_much_of_x_does_ship_have_in_cargo(get_ship_json, cargoSymbol)
    if units != 0:
      jettison_cargo(get_ship_json, cargoSymbol, units)

def fish_for(shipSymbol, cargoSymbol):
  survey_result = perform_survey(shipSymbol)
  surveys = survey_result['data']['surveys']  
  for survey in surveys:
    hit_count = 0
    size = survey['size']
    deposits = survey['deposits']
    deposits_length = len(deposits)
    for deposit in deposits:
      mineral_symbol = deposit['symbol']
      if mineral_symbol == cargoSymbol:
        hit_count += 1

    ratio = hit_count / deposits_length

    global BEST_SURVEY
    global BEST_SURVEY_SCORE
    


    rounded_ratio = round(ratio, 2)

    if ratio > BEST_SURVEY_SCORE:
      print(f'{INFO_STRING} {shipSymbol} {SURVEY_STRING} RESULT {rounded_ratio} NEW BEST')
      BEST_SURVEY = survey
      BEST_SURVEY_SCORE = round(rounded_ratio, 2)
    else:
      print(f'{INFO_STRING} {shipSymbol} {SURVEY_STRING} RESULT {rounded_ratio} DOES NOT BEAT {BEST_SURVEY_SCORE}')

def get_ship_capacity():
  return true

def is_ship_full(get_ship_json):
  capacity = get_ship_json['data']['cargo']['capacity'] 
  units = get_ship_json['data']['cargo']['units']
  if units == capacity:
    return True 
  return False

def is_ship_empty(get_ship_json):
  units = get_ship_json['data']['cargo']['units']
  if units == 0:
    return True
  return False

def is_ship_already_at_waypoint(get_ship_json, targetwaypointSymbol):
  data = get_ship_json['data']
  shipSymbol = get_ship_json['data']['symbol']
  nav = data['nav']
  waypointSymbol = nav['waypointSymbol']
  status = nav['status']
  if waypointSymbol == targetwaypointSymbol: 
    return True
  return False

def is_ship_in_orbit(get_ship_json):
  status = get_ship_json['data']['nav']['status']
  if status == 'IN_ORBIT':
    return True
  return False

def does_ship_need_to_dump_garbage(get_ship_json):
  shipSymbol = get_ship_json['data']['symbol']
  inventory = get_ship_json['data']['cargo']['inventory']
  for item in inventory:
    item_name = item['symbol']
    for garbage_item in GARBAGE:
      if item_name == garbage_item:
        return True    

  return False

def is_ship_in_transit(get_ship_json):
  status = get_ship_json['data']['nav']['status']
  shipSymbol = get_ship_json['data']['symbol']
  if status == "IN_TRANSIT":
    print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} IN_TRANSIT')
    return True
  return False
  
def is_ship_ready(get_ship_json):   
  shipSymbol = get_ship_json['data']['symbol']
  remainingSeconds = get_ship_json['data']['cooldown']['remainingSeconds']
  if remainingSeconds == 0:
    if is_ship_in_transit(get_ship_json):
      return False 
    return True
  print(f'{WARN_STRING} {shipSymbol} {COOLDOWN_STRING} {remainingSeconds} SECONDS REMAINING')
  return False
  

def does_ship_need_refuel(get_ship_json):
  shipSymbol = get_ship_json['data']['symbol']
  remaining_fuel = get_ship_json['data']['fuel']['current']
  fuel_capacity = get_ship_json['data']['fuel']['capacity']
  remaining_fuel_percentage = (remaining_fuel / fuel_capacity) * 100
 
  print(f'{INFO_STRING} {shipSymbol} {FUEL_STRING} {remaining_fuel_percentage}%')
 
  if remaining_fuel_percentage < REFUEL_PERCENT_THRESHOLD:
    return True
  return False
    

def basic_mining_loop(get_ship_json):

  shipSymbol = get_ship_json['data']['symbol'] 
  print(f'{INFO_STRING} {shipSymbol} {ASSIGNMENT_STRING} MINING')

  if is_ship_already_at_waypoint(get_ship_json, CONTRACT_DELIVERY_LOCATION):
    dock(get_ship_json)
    if not is_ship_empty(get_ship_json):      
      for cargoSymbol in SALE_GOODS:
        sell(get_ship_json, cargoSymbol, how_much_of_x_does_ship_have_in_cargo(get_ship_json, cargoSymbol))
    else:
      # ship is at DELIVERY waypoint, but its cargo hold is NOT full
      orbit(get_ship_json)
      move(get_ship_json, CONTRACT_ASTEROID_LOCATION)
  else:
    #ship is not at DELIVERY waypoint
    if is_ship_already_at_waypoint(get_ship_json, CONTRACT_ASTEROID_LOCATION):
      # ship is at ASTEROID waypoint
      if is_ship_full(get_ship_json):
        # and has a full hold
        print(f'{INFO_STRING} {shipSymbol} {CARGO_STRING} FULL')
        move(get_ship_json, CONTRACT_DELIVERY_LOCATION)

      if BEST_SURVEY_SCORE > 0.00:

        extract_resources_with_survey(get_ship_json, BEST_SURVEY)

      else:
        print(f'{WARN_STRING} {shipSymbol} {MINING_STRING} NO SURVEY NO POINT')
  
def basic_survey_loop(get_ship_json):
  shipSymbol = get_ship_json['data']['symbol']
  #print(f'{INFO_STRING} {shipSymbol} basic_survey_loop')

  if does_ship_need_refuel(get_ship_json):
    
 
  if is_ship_already_at_waypoint(get_ship_json, CONTRACT_ASTEROID_LOCATION):
    #print(f'{INFO_STRING} {shipSymbol} IS ALREADY AT {CONTRACT_ASTEROID_LOCATION}')
    if is_ship_in_orbit(get_ship_json):
      fish_for(shipSymbol, 'ALUMINUM_ORE')
    else:
      orbit(get_ship_json)
      fish_for(shipSymbol, 'ALUMINUM_ORE')
  else:
    print(f'{INFO_STRING} {shipSymbol} | IS NOT AT {CONTRACT_ASTEROID_LOCATION}')
    orbit(get_ship_json)
    move(get_ship_json, CONTRACT_ASTEROID_LOCATION)
    
def basic_command_loop(command_ship_json):
  shipSymbol = command_ship_json['data']['symbol']
  if BEST_SURVEY_SCORE < COMMAND_SHIP_DO_I_MINE_TOLERANCE:
    print(f'{INFO_STRING} {shipSymbol} {ASSIGNMENT_STRING} SURVEYING BECAUSE SURVEY BAD')
    basic_survey_loop(command_ship_json)
  else:
    print(f'{INFO_STRING} {shipSymbol} {ASSIGNMENT_STRING} MINING BECAUSE SURVEY GOOD')
    basic_mining_loop(command_ship_json)


# Pre-main for ad-hoc tests

#result = get_ship('TVRJ-3')
#prettyprint(result)
#result_json = json.loads(result)
#orbit(result_json)
#dump_garbage(result_json)

# Early exit for when Pre-main is in use.
#exit()

# MAIN
turn = 0

while True:
  turn += 1
  print(f'{INFO_STRING} TURN {turn} {TURN_STRING} START')

  # survey ship main
  survey_ship_status = get_ship(SURVEY_SHIP)
  survey_ship_json = json.loads(survey_ship_status)
  if is_ship_ready(survey_ship_json):
      print(f'{INFO_STRING} {SURVEY_SHIP} {ASSIGNMENT_STRING} SURVEYING')
      basic_survey_loop(survey_ship_json)

  # command ship main
  command_ship_status = get_ship(COMMAND_SHIP)
  command_ship_json = json.loads(command_ship_status)
  if is_ship_ready(command_ship_json):
    if does_ship_need_refuel(command_ship_json):
        dock(command_ship_json)
        refuel(command_ship_json)
    else:
      basic_command_loop(command_ship_json)
  
  # mining ship main
  for ship in mining_ships:
    mining_ship_status = get_ship(ship)
    mining_ship_json = json.loads(mining_ship_status)
    if is_ship_ready(mining_ship_json):
      if does_ship_need_refuel(mining_ship_json):
        dock(mining_ship_json)
        refuel(mining_ship_json)
      else:
        basic_mining_loop(mining_ship_json)
    
  print (f"""{INFO_STRING} TURN {turn} {TURN_STRING} END
  


                                         """)
  time.sleep(TURN_TIMER)