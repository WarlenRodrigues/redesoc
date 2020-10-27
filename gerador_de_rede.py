import json


class Gerador:

    def __init__(self):
        self.json_data = {}
        self.creators_game_info = {}
        self.creators_relationships = {}

    def get_data(self):
        with open('creators_mock.json') as json_file:
            self.json_data = json.load(json_file)

    def map_relations(self):

        # CREATING A JSON_DATA COPY IN ORDER TO AVOID FUTURE REDUNDANT CONNECTIONS
        json_data_copy = self.json_data.copy()

        # ITERATE TRHOUGH DEVS TO GET GAMES DONE
        for creator_id in self.json_data:

            # POPULATING DEV'S GAMES
            creator_games_ids = []
            for game in self.json_data[creator_id]['games']:
                creator_games_ids.append(game["id"])
            self.creators_game_info[creator_id] = creator_games_ids

            # DELETING DEV FROM COPY TO AVOID REDUNDANCY
            del json_data_copy[creator_id]

            # GETTING CO-WORKERS
            co_workers = []
            for creator in json_data_copy:
                # AVOIDING UNNECESSARY ITERATIONS TO SAVE RESOURCES
                if creator in co_workers:
                    break

                # MUST VERIFY ALL GAMES
                for game in json_data_copy[creator]["games"]:
                    if game["id"] in self.creators_game_info[creator_id]:
                        # JUST LIKE LINE 35
                        if creator in co_workers:
                            break
                        else:
                            co_workers.append(creator)

            self.creators_relationships[creator_id] = co_workers
        # print(self.creators_relationships)

    def generate_network(self):
        # CREATING GRAPH LEVEL
        f = open("network_data.gml", "w")
        f.write("graph [\n")
        f.write("   directed 0\n")
        f.write("\n")

        # CREATING NODES
        for node in self.creators_relationships:
            f.write("   node [\n")
            f.write("       id " + node + "\n")
            f.write("   ]\n")

        # CREATE CONNECTION
        for source in self.creators_relationships:
            for target in self.creators_relationships[source]:
                f.write("   edge [\n")
                f.write("       source " + source + "\n")
                f.write("       target " + target + "\n")
                f.write("   ]\n")

        f.write("]")
        f.close()


gerador = Gerador()
gerador.get_data()
gerador.map_relations()
gerador.generate_network()
