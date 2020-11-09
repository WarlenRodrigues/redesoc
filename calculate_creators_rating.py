import json


def add_creators_ranking(creatorsJson: json, gamesJson: json):
    filteredCreators = creatorsJson.copy()
    remove_creators_list = []
    index = 0
    for creator_id in creatorsJson.keys():
        creator = creatorsJson[creator_id]
        creator_games_count = creator['games_count']
        creator_games = creator['games']
        if creator_games_count == 0 and len(creator_games) == 0:
            remove_creators_list.append(creator_id)
        else:
            games_rating = []
            new_creators_game = []

            for creator_game in creator_games:
                game_id = str(creator_game['id'])
                if game_id in gamesJson.keys():
                    game = gamesJson[game_id]
                    games_ratings_count = game['ratings_count']
                    game_rating = game['rating']
                    if games_ratings_count > 0:
                        games_rating.append(game_rating)
                        new_creators_game.append(creator_game)
                else:
                    print(f'Game no in games: ID {game_id}')
                    with open('missing_games.txt', 'a') as file:
                      file.write(f'{game_id},\n')


            if len(new_creators_game) > 0:
                creator['games'] = new_creators_game
                creator_rating = sum(games_rating) / \
                    len(games_rating) if len(games_rating) else 0
                creator['rating'] = creator_rating
                filteredCreators[creator_id] = creator
            else:
                if creator_id not in remove_creators_list:
                    remove_creators_list.append(creator_id)


        print(f'{index}/{len(creatorsJson.keys())}')
        index += 1


    for id in remove_creators_list:
        if id in filteredCreators:
            del filteredCreators[id]

    try:
        with open('creators_filtered.json', 'w') as file:
            file.write(json.dumps(filteredCreators, indent=2, sort_keys=True))

    except IOError:
        print(f'ERROR writing creators_filtered')

    return filteredCreators


oldCreators = {}
with open('creators.json', 'r') as file:
    oldCreators = json.load(file)

gamesJson = {}
with open('games.json', 'r') as file:
    gamesJson = json.load(file)


add_creators_ranking(oldCreators, gamesJson)