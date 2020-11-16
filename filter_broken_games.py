import json
MIN_RATING = 0.005

brokenGames = [
    '56170',
    '28523',
    '56171'
]

oldCreators = {}
with open('creators.json', 'r') as file:
    oldCreators = json.load(file)


errorCount = {
  'min_rating': 0,
  'rating_not_in_gamesJson': 0,
  'not_in_gamesJson': 0,
  'game_in_brokenGames': 0,
  'no_games_count': 0,
}
gamesJson = {}
with open('games.json', 'r') as file:
    gamesJson = json.load(file)

filteredCreators = {}
filteredGames = {}
for creator_id in oldCreators.keys():
    creator = oldCreators[creator_id]
    creator_games = creator['games']

    games_ratings = []
    new_creator_games = []
    for game in creator_games:
        game_id = str(game['id'])
        if game_id not in brokenGames:
            if game_id in gamesJson:
                if 'rating' in gamesJson[game_id]:
                    if gamesJson[game_id]['rating'] > MIN_RATING:
                      games_ratings.append(gamesJson[game_id]['rating'])
                      new_creator_games.append(game)
                      filteredGames[game_id]: gamesJson[game_id]

    games_count = len(new_creator_games)
    if games_count > 0:
        creator_rating = sum(games_ratings) / games_count
        creator['rating'] = creator_rating
        creator['games'] = new_creator_games
        creator['games_count'] = games_count
        filteredCreators[str(creator_id)] = creator
try:
    with open('creators_filtered_copy_2.json', 'w') as file:
        print(f'DELETOU: {len(oldCreators.keys()) - len(filteredCreators.keys())} creators')
        file.write(json.dumps(filteredCreators, indent=2, sort_keys=True))
except IOError:
    print(f'ERROR writing creators_filtered')

try:
    with open('creators_games.json', 'w') as file:
        print(f'DELETOU: {len(gamesJson.keys()) - len(filteredGames.keys())} games')
        file.write(json.dumps(filteredGames, indent=2, sort_keys=True))
except IOError:
    print(f'ERROR writing creators_games')
