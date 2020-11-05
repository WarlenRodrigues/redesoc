import json
import credentials
import requests
import numpy as np

URL = 'https://api.rawg.io/api/'

API_KEY = credentials.get_api_key()

def printJson(obj):
  print(json.dumps(obj, indent=2, sort_keys=True))

def filter_creators_without_games(oldCreators: json):
  filteredCreators = oldCreators.copy()
  remove_list = []
  for creator_id in oldCreators.keys():
    creator = oldCreators[creator_id]
    creator_games_count = creator['games_count']
    creator_games = creator['games']
    if creator_games_count == 0 and len(creator_games) == 0:
      remove_list.append(creator_id)

  for id in remove_list:
    if id in filteredCreators:
      del filteredCreators[id]

  with open('creators_filtered.json', 'w') as file:
    file.write(json.dumps(filteredCreators, indent=2, sort_keys=True))

  return filteredCreators



def getGameByCreatorId(creatorId, nextUrl):
    if not creatorId:
      return []
    else:
      url = f'https://api.rawg.io/api/games?key={API_KEY}&creators={creatorId}'
      response = requests.get(nextUrl or url)
      data = response.json()

      next = ''
      if data['next']:
        next = data['next']

      games = data['results']

      return games, next
    
def createGamesJsonUsingCreatorsJson(creatorsJson, games):
  gamesJson = games.copy()
  creators = creatorsJson.copy()
  index = 467
  creators_keys = sorted(creators.keys())[index:]
  for creator_id in creators_keys:
    print(f'Criador: {creator_id} ---- {index}/{len(creators.keys())}')
    creator = creators[creator_id]
    games_rating = []
    nextUrl = ''
    while True:
      games, next = getGameByCreatorId(creator['id'], nextUrl)
      
      for game in games:
        game_id = str(game['id'])
        games_ratings_count = game["ratings_count"]
        game_rating = game['rating']

        if games_ratings_count > 0:
          games_rating.append(game_rating)

          if game_id not in gamesJson:
            gamesJson[game_id] = game

      if next:
        nextUrl = next
      else:
        break
      
 
    creator_rating = sum(games_rating) / len(games_rating) if len(games_rating) else 0
    creator['rating'] = creator_rating
    index += 1

    with open('games.json', 'w') as file:
      file.write(json.dumps(gamesJson, indent=2, sort_keys=True))

  return creators






oldCreators = {}
with open('creators.json', 'r') as file:
  oldCreators = json.load(file)

gamesJson = {}
with open('games.json', 'r') as file:
  gamesJson = json.load(file)



print(f'filter_creators_without_games started')
newCreators = filter_creators_without_games(oldCreators)
print(f'filter_creators_without_games finished')

createGamesJsonUsingCreatorsJson(newCreators, gamesJson)


