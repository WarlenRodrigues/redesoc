import json
import credentials
import requests

def printJson(obj):
    print(json.dumps(obj, indent=2, sort_keys=True))

URL = 'https://api.rawg.io/api/'

API_KEY = credentials.get_api_key()

gamesJson = {}
with open('games_copy.json', 'r') as file:
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
      shouldSave = index % 100 == 0
      if shouldWrite or shouldSave:
        try:
          if shouldSave:
            print(f'Salvando mais 100 {id}\n')
            with open('games_copy2.json', 'w') as file:
              file.write(json.dumps(gamesJson))

          print(f'escrevendo jogo {id}\n')
          with open('games_copy.json', 'w') as file:
            file.write(json.dumps(gamesJson))
            shouldWrite = False
        except IOError:
          print(f'ERROR')

  index += 1
    