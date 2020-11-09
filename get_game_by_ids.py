import json
import credentials
import requests

def printJson(obj):
    print(json.dumps(obj, indent=2, sort_keys=True))

URL = 'https://api.rawg.io/api/'

API_KEY = credentials.get_api_key()

gamesJson = {}
with open('games.json', 'r') as file:
    gamesJson = json.load(file)

games_ids = []
with open('missing_games.txt', 'r') as file:
    games_ids = file.read().split(',\n')

index = 1
shouldWrite = False
for id in games_ids:
  try:

    print(f'ID: {index}/{len(games_ids)}')
    if str(id) in gamesJson:
      print(f'id em game json: {id}')
    else:
      url = f'https://api.rawg.io/api/games/{int(id)}?key={API_KEY}'
      print(url)
      response = requests.get(url)
      game = response.json()
      if 'id' in game:
        game_id = str(game['id'])
        print(f'game: {game_id}')
        if game_id in gamesJson:
          print(f'2- id em game json\n')
        else:
          shouldWrite = True
          gamesJson[game_id] = game

  finally:
      if shouldWrite:
        print(f'escrevendo jogo {id}\n')
        try:
          with open('games.json', 'w') as file:
            file.write(json.dumps(gamesJson, indent=2, sort_keys=True))
            shouldWrite = False
        except IOError:
          print(f'ERROR')

  index += 1
    