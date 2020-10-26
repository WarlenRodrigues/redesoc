import json


class Gerador:

    def __init__(self):
        self.json_data = {}
        self.creators_game_info = {}
        self.

    def get_data(self):
        with open('creators.json') as json_file:
            self.json_data = json.load(json_file)

    def map_relations(self):
        for creator_id in self.json_data:
            # print(data[p]['games'])
            creator_games_ids = []
            print(self.json_data[creator_id]["name"])
            for game in self.json_data[creator_id]['games']:
                print(game["id"])
            # print(creat)

    # def get_functions(self):
    #     for line in range(0, len(self.code)):
    #         parameters = self.code[line].split(" ")
    #         for parameter in parameters:
    #             if ":" in parameter:
    #                 self.functions[parameter.replace(":", "")] = (
    #                     bin(int(line))[2:].zfill(9))

    # def generate_bin_code(self):
    #     for item in self.binary:
    #         full_line = 'tmp({0}) := "'.format(item)
    #         for piece in self.binary[item]:
    #             full_line += piece
    #         print(full_line)


# INSTANTIATING ASSEMBLER
gerador = Gerador()
gerador.get_data()
gerador.map_relations()
# assembler.get_functions()
# assembler.replace_opcodes_and_registers()
# assembler.generate_bin_code()
