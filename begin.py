import requests
import json
import time
import io
from datetime import datetime,timedelta  
import os.path

###
CALLSIGN = 'TVRJ-TEST-144'
FACTION  = 'COSMIC'
DESIRED_SURVEYOR_SHIPS = 1
DESIRED_MINING_SHIPS = 1
COMMAND_SHIP_DO_I_MINE_TOLERANCE = 0.5
###

MINING_SHIPS = []
SURVEYOR_SHIPS = []

INFO_STRING  = 'INFO  |'
CONTENT_TYPE = 'application/json'
AUTHORIZATION_TOKEN_FILE_PATH = f'{CALLSIGN}_token.txt'

def does_token_authorization_token_file_exist():
  if os.path.isfile(AUTHORIZATION_TOKEN_FILE_PATH):
    return True
  return False
  
def read_existing_auth_token_file_into_memory():
  AUTH_TOKEN_FILE_READ  = open(AUTHORIZATION_TOKEN_FILE_PATH, 'r', newline='' )
  global AUTHORIZATION_TOKEN
  AUTHORIZATION_TOKEN = AUTH_TOKEN_FILE_READ.read().rstrip()
  global DEFAULT_HEADERS
  DEFAULT_HEADERS = {'Content-Type': f"{CONTENT_TYPE}", 'Authorization': f"Bearer {AUTHORIZATION_TOKEN}" }
  








REFUEL_PERCENT_THRESHOLD = 50
SURVEY_AGE_TOLERANCE = timedelta(minutes=3)
TURN_TIMER = 120


WARN_STRING  = 'WARN  |'
ERROR_STRING = 'ERROR |'


TURN_STRING       = ''
SPACER_STRING     = 'SPACER|-------------------------------------------------------------------'
MINING_STRING     = '| MINING     |'
ASSIGNMENT_STRING = '| ASSIGNMENT |'
TRANSIT_STRING    = '| TRANSIT    |'
FUEL_STRING       = '| FUEL       |'
SURVEY_STRING     = '| SURVEY     |'
COOLDOWN_STRING   = '| COOLDOWN   |'
CARGO_STRING      = '| CARGO      |'
SOLD_STRING       = '| SOLD       |'
REPORTING_STRING  = '| REPORTING  |'
LOCATION_STRING   = '| LOCATION   |'
STATUS_STRING     = '| STATUS     |'



BASE_URL = 'https://api.spacetraders.io/v2'











BEST_SURVEY = ''
BEST_SURVEY_SCORE = 0.00

HTTP_CALL_COUNTER = 0

# These get populated
HEADQUARTERS = ''
APPLICATION_HEADER = {'Content-Type': f"{CONTENT_TYPE}" }

def write_new_auth_token_file(payload):
  AUTH_TOKEN_FILE_WRITE = open(AUTHORIZATION_TOKEN_FILE_PATH, 'w', newline='' )
  AUTH_TOKEN_FILE_WRITE.write(payload)
  AUTH_TOKEN_FILE_WRITE.close()
  print(f'{INFO_STRING} WROTE NEW AUTH FILE')



def populate_contract_globals():
  response = requests.get(f'{BASE_URL}/my/contracts', headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = response.json()
  data = json_object['data']


  global CONTRACT_ID
  CONTRACT_ID = data[0]['id']

  global CONTRACT_HAS_BEEN_COMPLETED
  CONTRACT_HAS_BEEN_COMPLETED = data[0]['fulfilled']

  global CONTRACT_DELIVERY_LOCATION
  CONTRACT_DELIVERY_LOCATION = data[0]['terms']['deliver'][0]['destinationSymbol']

  global CONTRACT_MINERAL
  CONTRACT_MINERAL = data[0]['terms']['deliver'][0]['tradeSymbol']

def populate_locations(systemSymbol):
  global SURVEYOR_SHIP_BUYING_LOCATION
  SURVEYOR_SHIP_BUYING_LOCATION = find_shipyard_by_ship_type(CURRENT_SYSTEM, 'SHIP_SURVEYOR')

  global MINING_SHIP_BUYING_LOCATION
  MINING_SHIP_BUYING_LOCATION = find_shipyard_by_ship_type(CURRENT_SYSTEM, 'SHIP_MINING_DRONE')

  global PROBE_SHIP_BUYING_LOCATION
  PROBE_SHIP_BUYING_LOCATION = find_shipyard_by_ship_type(CURRENT_SYSTEM, 'SHIP_PROBE')

  global CONTRACT_ASTEROID_LOCATION
  CONTRACT_ASTEROID_LOCATION = find_nearby_asteroid(CURRENT_SYSTEM)



# This is user discretion. What are you looking for?
GARBAGE = ['QUARTZ_SAND', 'ICE_WATER', 'SILICON_CRYSTALS']
SALE_GOODS = ['COPPER_ORE', 'IRON_ORE', 'ALUMINUM_ORE']

def prettyprint(blob):
  json_object = json.loads(blob)
  json_formatted_str = json.dumps(json_object, indent=2)
  print(json_formatted_str)

def get_status():
  r = requests.get(f'{BASE_URL}', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
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
  payload = {"symbol": CALLSIGN, "faction": FACTION }
  r = requests.post(f'{BASE_URL}/register', json=payload, headers=APPLICATION_HEADER)
  json_object = json.loads(r.text)
  data = json_object['data']
  AUTHORIZATION_TOKEN = data['token']
  write_new_auth_token_file(AUTHORIZATION_TOKEN)

def my_agent():
  r = requests.get(f'{BASE_URL}/my/agent', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
 # prettyprint(r.text)
  json_object = json.loads(r.text)
  data = json_object['data']
  symbol = data['symbol']
  credits = data['credits']
  shipCount = data['shipCount']
  print(f'{INFO_STRING} CALLSIGN  | {symbol}')
  print(f'{INFO_STRING} CREDITS   | {credits}')
  print(f'{INFO_STRING} SHIPCOUNT | {shipCount}')
  
def waypoint(systemSymbol, waypointSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints/{waypointSymbol}', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  #prettyprint(r.text)

def accept_contract(contract_id):
  r = requests.post(f'{BASE_URL}/my/contracts/{contract_id}/accept', headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  #prettyprint(r.text)

def find_shipyards(systemSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints?traits=SHIPYARD', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  data = json_object['data']
  return data

def find_shipyard_by_ship_type(systemSymbol, shipType):
  shipyards = find_shipyards(systemSymbol)
  
  for shipyard in shipyards:
    shipyardSymbol = shipyard['symbol']

    available_ships = view_available_ships(systemSymbol, shipyardSymbol)

    shipTypes = available_ships['shipTypes']
      
    for buyableShipType in shipTypes:
      if buyableShipType['type'] == shipType:
        return shipyardSymbol

      
     

def find_a_market(systemSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints?traits=MARKETPLACE', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  data = json_object

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
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  return json_object['data']

def buy_ship(shipType, shipyardWaypointSymbol):
  payload = {'shipType': f"{shipType}", 'waypointSymbol': f"{shipyardWaypointSymbol}" }
  r = requests.post(f'{BASE_URL}/my/ships', json=payload, headers=DEFAULT_HEADERS) 
  json_object = json.loads(r.text)
  if r.status_code != 201:
    print('ERROR')
    print(r.text)
    print('ERROR')
    return r.text

  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1


  print(f'{INFO_STRING} PURCHASED {shipType} at {shipyardWaypointSymbol}')
  return json_object['data']

def my_ships():
  r = requests.get(f'{BASE_URL}/my/ships',  headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  return(json_object['data'])




def get_ship(shipSymbol):
  if DEFAULT_HEADERS == {}:
    print(f'{ERROR_STRING} DEFAULT HEADERS NULL - SOMETHING IS DEEPLY WRONG')
    exit()
  r = requests.get(f'{BASE_URL}/my/ships/{shipSymbol}',  headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  return(json_object['data'])

def find_nearby_asteroid(systemSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints?type=ENGINEERED_ASTEROID',  headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  data = json_object['data']
  item = data[0]['symbol']
  return item



def orbit(ship_data):
  shipSymbol = ship_data['symbol']
  role = ship_data['registration']['role']
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/orbit', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = r.json()
  data = json_object['data']
  status = data['nav']['status']
  nav = data['nav']
  print(f'{INFO_STRING} {role} | {shipSymbol} {TRANSIT_STRING} {status}')

def move(ship_data, waypointSymbol):
  shipSymbol = ship_data['symbol']
  role = ship_data['registration']['role']
  payload = {'waypointSymbol': f"{waypointSymbol}" }
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/navigate', json=payload, headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = r.json()

  destination_symbol = json_object['data']['nav']['route']['destination']['symbol']
  departure_symbol = json_object['data']['nav']['route']['departure']['symbol']
    
  print(f'{INFO_STRING} {role} | {shipSymbol} {TRANSIT_STRING} {departure_symbol} TO {destination_symbol}')

def dock(ship_data):
  shipSymbol = ship_data['symbol']
  role = ship_data['registration']['role']
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/dock', headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  destination = json_object['data']['nav']['route']['destination']['symbol']
  status = json_object['data']['nav']['status']
  print(f'{INFO_STRING} {role} | {shipSymbol} {TRANSIT_STRING} {status} AT {destination}')

def fuel_tank_free_space(ship_data):
  shipSymbol = ship_data['symbol']
  fuel = ship_data['fuel']

def refuel(ship_data):
    shipSymbol = ship_data['symbol']
    print(f'{INFO_STRING} {shipSymbol} {FUEL_STRING} REFUELLING')
    r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/refuel', headers=DEFAULT_HEADERS) 
    global HTTP_CALL_COUNTER
    HTTP_CALL_COUNTER += 1
    json_object = r.json()
    if r.status_code == 200:
      data = json_object['data']
      totalPrice = json_object['data']['transaction']['totalPrice']
      units = json_object['data']['transaction']['units']
      print(f'{INFO_STRING} {shipSymbol} {FUEL_STRING} REFUELLED AND PAID {totalPrice} FOR {units} OF FUEL')

def extract(miningShipSymbol):
    print(f'{miningShipSymbol} Extracting...')
    r = requests.post(f'{BASE_URL}/my/ships/{miningShipSymbol}/extract', headers=DEFAULT_HEADERS) 
    global HTTP_CALL_COUNTER
    HTTP_CALL_COUNTER += 1
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
      role = data['registration']['role']
      print(f'{role} {miningShipSymbol} {MINING_STRING} EXTRACTED {units} {mined_symbol} AND IS {capacity}/{max_capacity}')
      
def view_market_data(systemSymbol, waypointSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints/{waypointSymbol}/market', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  # ['data']['tradeGoods'] likely only exists if you have a ship at the waypoint.
  data = json_object['data']['imports']
  for item in data:
    print(f'{item["symbol"]}')
   # print(f'volume {item["tradeVolume"]}')
   # print(f'supply {item["supply"]}')
   # print(f'buy@  {item["purchasePrice"]}')
   # print(f'sell@ {item["sellPrice"]}')

      
def sell(ship_data, goodsSymbol, units):
  shipSymbol = ship_data['symbol']
  payload = {'symbol': f"{goodsSymbol}", 'units': f"{units}" }
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/sell', json=payload, headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
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
    global HTTP_CALL_COUNTER
    HTTP_CALL_COUNTER += 1
    prettyprint(r.text)

def fulfil_contract(contractId):
    r = requests.post(f'{BASE_URL}/my/contracts/{contractId}/fulfill', headers=DEFAULT_HEADERS) 
    global HTTP_CALL_COUNTER
    HTTP_CALL_COUNTER += 1
    prettyprint(r.text)

def jettison_cargo(ship_data, cargoSymbol, units):
  shipSymbol = ship_data['symbol']
  payload = {'shipSymbol': f"{shipSymbol}", 'symbol': f"{cargoSymbol}", 'units': f"{units}" }
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/jettison', json=payload, headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = r.json()
  if r.status_code != 200:
    error = json_object['error']
    message = error['message']
  max_capacity = ship_data['cargo']['capacity']
  capacity = ship_data['cargo']['units']
  role = ship_data['registration']['role']
  print(f'{INFO_STRING} {role} | {shipSymbol} {MINING_STRING} JETTISONED {units} {cargoSymbol} {capacity}/{max_capacity}')

def is_best_survey_expired():
  #print(f'{INFO_STRING} SURVEY CHECKING EXPIRATION')
  if BEST_SURVEY_SCORE == 0.00:
    print(f'{WARN_STRING} SURVEY NOT FOUND')
    return False
  time_now = datetime.now().isoformat()
  time_now_string = f"{time_now}Z"
  time_now_dt = datetime.strptime(time_now_string, "%Y-%m-%dT%H:%M:%S.%fZ")
  expiration = BEST_SURVEY['expiration']
  expiration_dt = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S.%fZ")
  remaining_time_dt = expiration_dt - time_now_dt 
  #print(f'{INFO_STRING} {SURVEY_STRING} {remaining_time_dt} REMAINING')
  if remaining_time_dt < SURVEY_AGE_TOLERANCE:
    print(f'{WARN_STRING} {SURVEY_STRING} EXPIRES SOON')
    purge_expired_survey()
    return True
  else:
    #print(f'{INFO_STRING}  {SURVEY_STRING} EXPIRATION WITHIN SURVEY_AGE_TOLERANCE')
    return False

def purge_expired_survey():
  global BEST_SURVEY
  global BEST_SURVEY_SCORE
  BEST_SURVEY = ''
  BEST_SURVEY_SCORE = 0.00
  print(f'{INFO_STRING}  {SURVEY_STRING} PURGED BECAUSE EXPIRING')

def perform_survey(shipSymbol):
  #print(f'{INFO_STRING} {shipSymbol} perform_survey')
  if is_best_survey_expired():
    purge_expired_survey
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/survey', headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = r.json()
  if r.status_code == 201:
    return json_object
  else:
    print(json_object['error']['message'])

def extract_resources_with_survey(ship_data, survey):
  shipSymbol = ship_data['symbol']
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/extract/survey', json=survey, headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
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
    role = ship_data['registration']['role']
    print(f'{INFO_STRING} {role} | {shipSymbol} {MINING_STRING} EXTRACTED {units} {mined_symbol} {capacity}/{max_capacity}')
    for garbageSymbol in GARBAGE:
      if mined_symbol == garbageSymbol:
        jettison_cargo(ship_data, mined_symbol, units)

def how_much_of_x_does_ship_have_in_cargo(ship_data, cargoSymbol):
  shipSymbol = ship_data['symbol']
  inventory = ship_data['cargo']['inventory']
  for item in inventory:
    if item['symbol'] == cargoSymbol:
      return item['units']
  return 0

def dump_garbage(ship_data):
  
  shipSymbol = ship_data['symbol']
  for cargoSymbol in GARBAGE:
    units = how_much_of_x_does_ship_have_in_cargo(ship_data, cargoSymbol)
    if units != 0:
      jettison_cargo(ship_data, cargoSymbol, units)

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
      print(f'{INFO_STRING} SURVEY SAYS {rounded_ratio} # NEW BEST #')
      BEST_SURVEY = survey
      BEST_SURVEY_SCORE = round(rounded_ratio, 2)
    else:
      print(f'{INFO_STRING} SURVEY RESULT {rounded_ratio} DOES NOT BEAT {BEST_SURVEY_SCORE}')

def get_ship_capacity():
  return True

def is_ship_full(ship_data):
  capacity = ship_data['cargo']['capacity'] 
  units = ship_data['cargo']['units']
  if units == capacity:
    return True 
  return False

def is_ship_empty(ship_data):
  units = ship_data['cargo']['units']
  if units == 0:
    return True
  return False

def is_ship_already_at_waypoint(ship_data, targetwaypointSymbol):
  data = ship_data
  shipSymbol = ship_data['symbol']
  nav = data['nav']
  waypointSymbol = nav['waypointSymbol']
  status = nav['status']
  if waypointSymbol == targetwaypointSymbol: 
    return True
  return False

def is_ship_in_orbit(ship_data):
  status = ship_data['nav']['status']
  if status == 'IN_ORBIT':
    return True
  return False

def does_ship_need_to_dump_garbage(ship_data):
  shipSymbol = ship_data['symbol']
  inventory = ship_data['cargo']['inventory']
  for item in inventory:
    item_name = item['symbol']
    for garbage_item in GARBAGE:
      if item_name == garbage_item:
        return True    

  return False

def is_ship_in_transit(ship_data):
  status = ship_data['nav']['status']
  shipSymbol = ship_data['symbol']
  role = ship_data['registration']['role']
  if status == "IN_TRANSIT":
    print(f'{INFO_STRING} {role} | {shipSymbol} {TRANSIT_STRING} IN_TRANSIT')
    return True
  return False

def is_ship_docked(ship_data):
  status = ship_data['nav']['status']
  shipSymbol = ship_data['symbol']
  role = ship_data['registration']['role']
  if status == "DOCKED":
    print(f'{INFO_STRING} {role} | {shipSymbol} {TRANSIT_STRING} DOCKED')
    return True
  return False  

def is_ship_ready(ship_data): 
  shipSymbol = ship_data['symbol']
  role = ship_data['registration']['role']
  remainingSeconds = ship_data['cooldown']['remainingSeconds']
  if remainingSeconds == 0:
    if is_ship_in_transit(ship_data):
      return False 
    return True
  print(f'{WARN_STRING} {role} | {shipSymbol} {COOLDOWN_STRING} {remainingSeconds} SECONDS REMAINING')
  return False

def status_report(ship):
  shipSymbol     = ship['symbol']
  remaining_fuel = ship['fuel']['current']
  fuel_capacity  = ship['fuel']['capacity']
  status         = ship['nav']['status']
  max_capacity   = ship['cargo']['capacity']
  cargo_units    = ship['cargo']['units']
  role           = ship['registration']['role']
  location       = ship['nav']['waypointSymbol']

  print(SPACER_STRING)
  print(f'{INFO_STRING} {role} | {shipSymbol}')
  print(f'{INFO_STRING} {role} | {shipSymbol} {LOCATION_STRING} {location}')
  print(f'{INFO_STRING} {role} | {shipSymbol} {STATUS_STRING} {status}')
  print(f'{INFO_STRING} {role} | {shipSymbol} {FUEL_STRING} {remaining_fuel}/{fuel_capacity}')
  print(f'{INFO_STRING} {role} | {shipSymbol} {CARGO_STRING} {cargo_units}/{max_capacity}')


def does_ship_need_refuel(ship_data):
  shipSymbol = ship_data['symbol']
  remaining_fuel = ship_data['fuel']['current']
  fuel_capacity = ship_data['fuel']['capacity']
  remaining_fuel_percentage = (remaining_fuel / fuel_capacity) * 100 
  if remaining_fuel_percentage < REFUEL_PERCENT_THRESHOLD:
    return True
  return False
    
def is_probe_at_surveyor_buying_location(ship_data):
  shipLocation = ship_data['nav']['waypointSymbol']
  if shipLocation != SURVEYOR_SHIP_BUYING_LOCATION:
    return False
  return True

def is_probe_at_mining_ship_buying_location(ship_data):
  shipLocation = ship_data['nav']['waypointSymbol']
  if shipLocation != MINING_SHIP_BUYING_LOCATION:
    return False
  return True

def purchase_surveyor():
  buy_ship_result = buy_ship('SHIP_SURVEYOR', SURVEYOR_SHIP_BUYING_LOCATION)

  global SURVEYOR_SHIPS
  shipSymbol = buy_ship_result['ship']['symbol']
  SURVEYOR_SHIPS.append(shipSymbol)
  print(f'{INFO_STRING} PURCHASED SURVEYOR')

def purchase_miner():
  buy_ship_result = buy_ship('SHIP_MINING_DRONE', MINING_SHIP_BUYING_LOCATION)
  global MINING_SHIPS
  shipSymbol = buy_ship_result['ship']['symbol']
  MINING_SHIPS.append(shipSymbol)
  print(f'{INFO_STRING} PURCHASED MINER')

# ROLE LOOPS


def basic_mining_loop(ship_data, asteroid_location):
  print(SPACER_STRING)
  status_report(ship_data)
  shipSymbol = ship_data['symbol'] 
  role = ship_data['registration']['role']
  print(f'{INFO_STRING} {role} | {shipSymbol} {ASSIGNMENT_STRING} MINING')

  if is_ship_already_at_waypoint(ship_data, CONTRACT_DELIVERY_LOCATION):
    print(f'{INFO_STRING} {role} | {shipSymbol} IS ALREADY AT CONTRACT_DELIVERY_LOCATION')
    if not is_ship_docked(ship_data):
      print(f'{INFO_STRING} {role} | {shipSymbol} DOCKING')
      dock(ship_data)

    if not is_ship_empty(ship_data):      
      for cargoSymbol in SALE_GOODS:
        sell(ship_data, cargoSymbol, how_much_of_x_does_ship_have_in_cargo(ship_data, cargoSymbol))
    orbit(ship_data)
    move(ship_data, asteroid_location)
  else:
    #ship is not at DELIVERY waypoint
    if is_ship_already_at_waypoint(ship_data, asteroid_location):
      if is_ship_docked(ship_data):
        orbit(ship_data)
      print(f'{INFO_STRING} {role} | {shipSymbol} | SITUATION  | ON SITE AT CONTRACT_ASTEROID_LOCATION')
      # ship is at ASTEROID waypoint
      if is_ship_full(ship_data):
        # and has a full hold
        print(f'{INFO_STRING} {role} | {shipSymbol} {CARGO_STRING} FULL')
        move(ship_data, CONTRACT_DELIVERY_LOCATION)

      if BEST_SURVEY_SCORE > 0.00:

        extract_resources_with_survey(ship_data, BEST_SURVEY)

      else:
        print(f'{WARN_STRING} {role} | {shipSymbol} {MINING_STRING} NO SURVEY NO POINT')
    else:
      if is_ship_docked:
        orbit(ship_data)
      move(ship_data, CONTRACT_ASTEROID_LOCATION)

def basic_survey_loop(ship_data, asteroid_location):
  print(SPACER_STRING)
  status_report(ship_data)
  shipSymbol = ship_data['symbol']
  if is_ship_already_at_waypoint(ship_data, asteroid_location):
    if is_ship_in_orbit(ship_data):
      fish_for(shipSymbol, CONTRACT_MINERAL)
    else:
      orbit(ship_data)
      fish_for(shipSymbol, CONTRACT_MINERAL)
  else:
    orbit(ship_data)
    move(ship_data, asteroid_location)
    
def basic_command_loop(ship_data):
  print(SPACER_STRING)
  shipSymbol = ship_data['symbol']
  shipRole   = ship_data['registration']['role']
  if BEST_SURVEY_SCORE < COMMAND_SHIP_DO_I_MINE_TOLERANCE:
    print(f'{INFO_STRING} {shipRole} | {shipSymbol} {ASSIGNMENT_STRING} SURVEYING BECAUSE SURVEY BAD')
    basic_survey_loop(ship_data, CONTRACT_ASTEROID_LOCATION)
  else:
    print(f'{INFO_STRING} {shipRole} | {shipSymbol} {ASSIGNMENT_STRING} MINING BECAUSE SURVEY GOOD')
    basic_mining_loop(ship_data, CONTRACT_ASTEROID_LOCATION)

def basic_probe_loop(ship_data):
  status_report(ship_data)
  shipSymbol = ship_data['symbol']
  shipRole   = ship_data['registration']['role']
  if len(SURVEYOR_SHIPS) < DESIRED_SURVEYOR_SHIPS:
    if is_probe_at_surveyor_buying_location(ship_data):
      if is_ship_docked(ship_data):
        purchase_surveyor()
      else:
        dock(ship_data)
    else:
      if is_ship_docked(ship_data):
        orbit(ship_data)# goto surveyor
      move(ship_data, SURVEYOR_SHIP_BUYING_LOCATION)
      print(f'{INFO_STRING} {shipRole} {shipSymbol} {ASSIGNMENT_STRING} HEADING TO SURVEYOR_SHIP_BUYING_LOCATION')

  if len(MINING_SHIPS) < DESIRED_MINING_SHIPS:
    if is_probe_at_mining_ship_buying_location(ship_data):
      if is_ship_docked(ship_data):
        purchase_miner()
      else:
        dock(ship_data)
  # probe ship is not at surveyor buying location
    else:
      if is_ship_docked(ship_data):
        orbit(ship_data)# goto surveyor
    
      move(ship_data, SURVEYOR_SHIP_BUYING_LOCATION)
      print(f'{INFO_STRING} {shipRole} {shipSymbol} {ASSIGNMENT_STRING} HEADING TO MINER_SHIP_BUYING_LOCATION')

  # buy surveyor
  # find miner
  # goto miner
  # buy miner








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

# This happens once on startup.
if does_token_authorization_token_file_exist():
  print(f'{INFO_STRING} AUTH FILE FOUND') 
  print(f'{INFO_STRING} INITIATE INITIALIZATION')  
  read_existing_auth_token_file_into_memory()


else:
  print(f'{INFO_STRING} AUTH FILE ABSENT')
  print(f'{INFO_STRING} INITIATE INITIAL INITIALIZATION')  
  create_agent()
  read_existing_auth_token_file_into_memory()

print(SPACER_STRING)

populate_contract_globals()

all_ships_json = my_ships()
for ship in all_ships_json:
  shipSymbol = ship['symbol']
  CURRENT_SYSTEM = ship['nav']['systemSymbol']
  shipRole = ship['registration']['role']
  if shipRole == 'COMMAND':
    COMMAND_SHIP = shipSymbol
  if shipRole == 'SATELLITE':
    PROBE_SHIP = shipSymbol
  if shipRole == 'EXCAVATOR':
    MINING_SHIPS.append(shipSymbol)
  if shipRole == 'SURVEYOR':
    SURVEYOR_SHIPS.append(shipSymbol)

populate_locations(CURRENT_SYSTEM)






# Infinite loop to simulate turns of length TURN_LENGTH
while True:

  # increment turn number
  turn += 1

  # reset per turn HTTP CALL COUNTER
  HTTP_CALL_COUNTER = 0

  # inform the user that the turn is beginning
  print(f'{INFO_STRING} TURN {turn} {TURN_STRING} START --------------------------')

  # probe ship main
  probe_ship_json = get_ship(PROBE_SHIP)
  if is_ship_ready(probe_ship_json):
    basic_probe_loop(probe_ship_json)

  print(SPACER_STRING)

  # surveyor ship main
  if len(SURVEYOR_SHIPS) > 0:
    for ship in SURVEYOR_SHIPS:
      surveyor_ship_data = get_ship(ship)
      if is_ship_ready(surveyor_ship_data):
        if does_ship_need_refuel(surveyor_ship_data):
          dock(surveyor_ship_data)
          refuel(surveyor_ship_data)
        else:
          basic_survey_loop(surveyor_ship_data, CONTRACT_ASTEROID_LOCATION)

  print(SPACER_STRING)

  # Command ship main
  command_ship_json = get_ship(COMMAND_SHIP)
  if is_ship_ready(command_ship_json):
    if does_ship_need_refuel(command_ship_json):
        dock(command_ship_json)
        refuel(command_ship_json)
    else:
      basic_command_loop(command_ship_json)

  print(SPACER_STRING)

  # mining ship main
  if len(MINING_SHIPS) > 0:
    for ship in MINING_SHIPS:
      mining_ship_json = get_ship(ship)
      if is_ship_ready(mining_ship_json):
        if does_ship_need_refuel(mining_ship_json):
          dock(mining_ship_json)
          refuel(mining_ship_json)
        else:
          basic_mining_loop(mining_ship_json, CONTRACT_ASTEROID_LOCATION)
  
  print(SPACER_STRING)
  print (f'{INFO_STRING} TURN {turn} {TURN_STRING} END -----------------------------')
  print(SPACER_STRING)
  print (f'{INFO_STRING} HTTP COST | {HTTP_CALL_COUNTER/2}/m')

  my_agent()
  print(SPACER_STRING)
  print (f"""
  

                                         """)


  time.sleep(TURN_TIMER)