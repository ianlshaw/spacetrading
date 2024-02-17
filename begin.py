import requests
import json
import time
import io
from datetime import datetime,timedelta  
import os.path

###
CALLSIGN = 'TVRJ-TEST-136'
FACTION  = 'COSMIC'
DESIRED_SURVEYORS = 1
DESIRED_MINING_SHIPS = 5
###

INFO_STRING  = 'INFO  |'
ORCHESTRATOR_STRING = 'ORCHESTRATOR'
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
  







COMMAND_SHIP_DO_I_MINE_TOLERANCE = 0.5
REFUEL_PERCENT_THRESHOLD = 50
SURVEY_AGE_TOLERANCE = timedelta(minutes=3)
TURN_TIMER = 120

HAS_SURVEYOR_BEEN_PURCHASED = False
HAS_FIRST_MINER_BEEN_PURCHASED = False
HAS_HAULER_BEEN_PURCHASED = False


WARN_STRING  = 'WARN  |'
ERROR_STRING = 'ERROR |'


TURN_STRING       = '|------------------------'

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
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} WROTE NEW AUTH FILE')



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
  global SURVEYOR_BUYING_LOCATION
  SURVEYOR_BUYING_LOCATION = find_shipyard_by_ship_type(CURRENT_SYSTEM, 'SHIP_SURVEYOR')

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
  json_object = r.json()
  AUTHORIZATION_TOKEN = json_object['token']
  write_new_auth_token_file(AUTHORIZATION_TOKEN)

# early exit to test new CALLSIGN creation.

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
  print(f'{symbol}')
  print(f'Balance: {credits}')
  print(f'shipCount {shipCount}')
  
def waypoint(systemSymbol, waypointSymbol):
  r = requests.get(f'{BASE_URL}/systems/{systemSymbol}/waypoints/{waypointSymbol}', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  prettyprint(r.text)

def accept_contract(contract_id):
  r = requests.post(f'{BASE_URL}/my/contracts/{contract_id}/accept', headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  prettyprint(r.text)

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
  if r.status_code != 201:
    print('ERROR')
    print(r.text)
    print('ERROR')
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  print(f'{INFO_STRING} PURCHASED {shipType} at {shipyardWaypointSymbol}')

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
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/orbit', headers=DEFAULT_HEADERS)
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = r.json()
  if r.status_code != 200:
    print(json_object['error']['message'])
    return
  status = json_object['data']['nav']['status']
  nav = json_object['data']['nav']
  print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} {status}')

def move(ship_data, waypointSymbol):
  shipSymbol = ship_data['symbol']
  payload = {'waypointSymbol': f"{waypointSymbol}" }
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/navigate', json=payload, headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = r.json()

  if r.status_code != 200:
    print(json_object['error']['message'])
    return

  destination_symbol = json_object['data']['nav']['route']['destination']['symbol']
  departure_symbol = json_object['data']['nav']['route']['departure']['symbol']
    
  print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} {departure_symbol} TO {destination_symbol}')

def dock(ship_data):
  shipSymbol = ship_data['symbol']
  r = requests.post(f'{BASE_URL}/my/ships/{shipSymbol}/dock', headers=DEFAULT_HEADERS) 
  global HTTP_CALL_COUNTER
  HTTP_CALL_COUNTER += 1
  json_object = json.loads(r.text)
  if r.status_code != 200:
    print(json_object['error']['message'])
    return
  destination = json_object['data']['nav']['route']['destination']['symbol']
  status = json_object['data']['nav']['status']
  print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} {status} AT {destination}')

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
      print(f'{miningShipSymbol} {MINING_STRING} EXTRACTED {units} {mined_symbol} AND IS {capacity}/{max_capacity}')
      
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
  print(f'{INFO_STRING} {shipSymbol} {MINING_STRING} JETTISONED {units} {cargoSymbol} {capacity}/{max_capacity}')

def is_best_survey_expired():
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} {SURVEY_STRING} CHECKING EXPIRATION')
  if BEST_SURVEY_SCORE == 0.00:
    print(f'{WARN_STRING} {ORCHESTRATOR_STRING} {SURVEY_STRING} NOT FOUND')
    return False
  time_now = datetime.now().isoformat()
  time_now_string = f"{time_now}Z"
  time_now_dt = datetime.strptime(time_now_string, "%Y-%m-%dT%H:%M:%S.%fZ")
  expiration = BEST_SURVEY['expiration']
  expiration_dt = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S.%fZ")
  remaining_time_dt = expiration_dt - time_now_dt 
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} {SURVEY_STRING} {remaining_time_dt} REMAINING')
  if remaining_time_dt < SURVEY_AGE_TOLERANCE:
    #print(f'{WARN_STRING} {ORCHESTRATOR_STRING} {SURVEY_STRING} EXPIRES SOON')
    purge_expired_survey()
    return True
  else:
    #print(f'{INFO_STRING} {ORCHESTRATOR_STRING} {SURVEY_STRING} EXPIRATION WITHIN SURVEY_AGE_TOLERANCE')
    return False

def purge_expired_survey():
  global BEST_SURVEY
  global BEST_SURVEY_SCORE
  BEST_SURVEY = ''
  BEST_SURVEY_SCORE = 0.00
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} {SURVEY_STRING} PURGED BECAUSE EXPIRING')


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
    print(f'{INFO_STRING} {shipSymbol} {MINING_STRING} EXTRACTED {units} {mined_symbol} {capacity}/{max_capacity}')
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
      print(f'{INFO_STRING} {shipSymbol} {SURVEY_STRING} SAYS {rounded_ratio} NEW BEST')
      BEST_SURVEY = survey
      BEST_SURVEY_SCORE = round(rounded_ratio, 2)
    else:
      print(f'{INFO_STRING} {shipSymbol} {SURVEY_STRING} RESULT {rounded_ratio} DOES NOT BEAT {BEST_SURVEY_SCORE}')

def get_ship_capacity():
  return true

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
  if status == "IN_TRANSIT":
    print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} IN_TRANSIT')
    return True
  return False

def is_ship_docked(ship_data):
  status = ship_data['nav']['status']
  shipSymbol = ship_data['symbol']
  if status == "DOCKED":
    print(f'{INFO_STRING} {shipSymbol} {TRANSIT_STRING} DOCKED')
    return True
  return False  

def is_ship_ready(ship_data): 
 
  shipSymbol = ship_data['symbol']
  remainingSeconds = ship_data['cooldown']['remainingSeconds']
  if remainingSeconds == 0:
    if is_ship_in_transit(ship_data):
      return False 
    return True
  print(f'{WARN_STRING} {shipSymbol} {COOLDOWN_STRING} {remainingSeconds} SECONDS REMAINING')
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

  print(f'{INFO_STRING} {shipSymbol} | {role}')
  print(f'{INFO_STRING} {shipSymbol} {LOCATION_STRING} {location}')
  print(f'{INFO_STRING} {shipSymbol} {FUEL_STRING} {remaining_fuel}/{fuel_capacity}')
  print(f'{INFO_STRING} {shipSymbol} {CARGO_STRING} {cargo_units}/{max_capacity}')
  print(f'{INFO_STRING} ---------------------------------------------')

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
  if shipLocation != SURVEYOR_BUYING_LOCATION:
    return False
  return True

def purchase_surveyor():
  buy_ship('SHIP_SURVEYOR', SURVEYOR_BUYING_LOCATION)
  global HAS_SURVEYOR_BEEN_PURCHASED
  HAS_SURVEYOR_BEEN_PURCHASED = True
  


# ROLE LOOPS


def basic_mining_loop(ship_data, asteroid_location):

  shipSymbol = ship_data['symbol'] 
  print(f'{INFO_STRING} {shipSymbol} {ASSIGNMENT_STRING} MINING')

  if is_ship_already_at_waypoint(ship_data, CONTRACT_DELIVERY_LOCATION):
    if not is_ship_docked(ship_data):
      dock(ship_data)

    if not is_ship_empty(ship_data):      
      for cargoSymbol in SALE_GOODS:
        sell(ship_data, cargoSymbol, how_much_of_x_does_ship_have_in_cargo(ship_data, cargoSymbol))
    orbit(ship_data)
    move(ship_data, asteroid_location)

  else:
    #ship is not at DELIVERY waypoint
    if is_ship_already_at_waypoint(ship_data, asteroid_location):
      # ship is at ASTEROID waypoint
      if is_ship_full(ship_data):
        # and has a full hold
        print(f'{INFO_STRING} {shipSymbol} {CARGO_STRING} FULL')
        move(ship_data, CONTRACT_DELIVERY_LOCATION)

      if BEST_SURVEY_SCORE > 0.00:

        extract_resources_with_survey(ship_data, BEST_SURVEY)

      else:
        print(f'{WARN_STRING} {shipSymbol} {MINING_STRING} NO SURVEY NO POINT')
  
def basic_survey_loop(ship_data, asteroid_location):
  shipSymbol = ship_data['symbol']
  if is_ship_already_at_waypoint(ship_data, asteroid_location):
    if is_ship_in_orbit(ship_data):
      fish_for(shipSymbol, CONTRACT_MINERAL)
    else:
      orbit(ship_data)
      fish_for(shipSymbol, CONTRACT_MINERAL)
  else:
    print(f'{INFO_STRING} {shipSymbol} | IS NOT AT {asteroid_location}')
    orbit(ship_data)
    move(ship_data, asteroid_location)
    
def basic_command_loop(command_ship_json):
  shipSymbol = command_ship_json['symbol']
  if BEST_SURVEY_SCORE < COMMAND_SHIP_DO_I_MINE_TOLERANCE:
    print(f'{INFO_STRING} {shipSymbol} {ASSIGNMENT_STRING} SURVEYING BECAUSE SURVEY BAD')
    basic_survey_loop(command_ship_json, CONTRACT_ASTEROID_LOCATION)
  else:
    print(f'{INFO_STRING} {shipSymbol} {ASSIGNMENT_STRING} MINING BECAUSE SURVEY GOOD')
    basic_mining_loop(command_ship_json, CONTRACT_ASTEROID_LOCATION)

def basic_probe_loop(ship_data):
  # IS SURVEYOR PURCHASED?
  if not HAS_SURVEYOR_BEEN_PURCHASED:
    if is_probe_at_surveyor_buying_location(ship_data):
      
      if is_ship_docked(ship_data):
        print('purchase_surveyor ')
        #purchase_surveyor()
      else:
        dock(ship_data)
        purchase_surveyor()
    # probe ship is not at surveyor buying location
    else:
      if is_ship_docked(ship_data):
        orbit(ship_data)# goto surveyor
      
      move(ship_data, SURVEYOR_BUYING_LOCATION)
      print('en route to surveyor boss')
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
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} AUTH FILE FOUND') 
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} INITIATE INITIALIZATION')  
  read_existing_auth_token_file_into_memory()


else:
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} AUTH FILE ABSENT')
  print(f'{INFO_STRING} {ORCHESTRATOR_STRING} INITIATE INITIAL INITIALIZATION')  
  create_agent()
  read_existing_auth_token_file_into_memory()

print('-----------------------------------------------------')

populate_contract_globals()

all_ships_json = my_ships()
for ship in all_ships_json:
  shipSymbol = ship['symbol']
  status_report(ship)
  CURRENT_SYSTEM = ship['nav']['systemSymbol']
  shipRole = ship['registration']['role']
  if shipRole == 'COMMAND':
    COMMAND_SHIP = shipSymbol
  if shipRole == 'SATELLITE':
    PROBE_SHIP = shipSymbol

populate_locations(CURRENT_SYSTEM)






# Infinite loop to simulate turns of length TURN_LENGTH
while True:

  # increment turn number
  turn += 1

  # reset per turn HTTP CALL COUNTER
  HTTP_CALL_COUNTER = 0

  # inform the user that the turn is beginning
  print(f'{INFO_STRING} TURN {turn} {TURN_STRING} START')

  # survey ship main
  if HAS_SURVEYOR_BEEN_PURCHASED:
    survey_ship_json = get_ship(SURVEY_SHIP)
    
    if is_ship_ready(survey_ship_json):
        print(f'{INFO_STRING} {SURVEY_SHIP} {ASSIGNMENT_STRING} SURVEYING')
        basic_survey_loop(survey_ship_json, CONTRACT_ASTEROID_LOCATION)
  
  

  probe_ship_json = get_ship(PROBE_SHIP)
  
  
  if is_ship_ready(probe_ship_json):
    basic_probe_loop(probe_ship_json)



  # Command ship main
  command_ship_json = get_ship(COMMAND_SHIP)
  

  if is_ship_ready(command_ship_json):
    if does_ship_need_refuel(command_ship_json):
        dock(command_ship_json)
        refuel(command_ship_json)
    else:
      basic_command_loop(command_ship_json)

  # mining ship main
  if HAS_FIRST_MINER_BEEN_PURCHASED:
    for ship in mining_ships:
      mining_ship_status = get_ship(ship)
      mining_ship_json = json.loads(mining_ship_status)
      if is_ship_ready(mining_ship_json):
        if does_ship_need_refuel(mining_ship_json):
          dock(mining_ship_json)
          refuel(mining_ship_json)
        else:
          basic_mining_loop(mining_ship_json, CONTRACT_ASTEROID_LOCATION)
    
  print (f'{INFO_STRING} TURN {turn} {TURN_STRING} END')
  print (f' ')
  print (f'{INFO_STRING} HTTP CALLS {HTTP_CALL_COUNTER/2}/m')
  my_agent()
  print (f"""
  

                                         """)


  time.sleep(TURN_TIMER)