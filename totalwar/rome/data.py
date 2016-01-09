from .utilities import *
import struct

class DataSaveFile:

    def __init__(self, structured_save_file):
        self.structured_save_file = structured_save_file

        self.starter_section = DataStarterSection(self.structured_save_file.starter_section)



class DataStarterSection:
    def __init__(self, starter_section):
        #Process first record
        self.first_record = {}
        self.first_record["campaign_difficulty"] = four_to_one(starter_section[0][584:588])
        self.first_record["battle_difficulty"] = four_to_one(starter_section[0][588:592])
        self.first_record["faction_id"] = starter_section[0][1273]
        self.first_record["year"] = struct.unpack("i", starter_section[0][1276:1280])[0]

        #Process second record
        self.second_record = {}
        first_length = starter_section[1][4] * 2
        self.second_record["path"] = starter_section[1][6:6 + first_length][::2].decode()
        second_length = starter_section[1][6 + first_length] * 2
        self.second_record["campaign"] = starter_section[1][
         8 + first_length: 8 + first_length + second_length][::2].decode()


        #Process fourth record
        self.fourth_record = {}
        self.fourth_record["turn_number"] = four_to_one(starter_section[3][5:9])
        self.fourth_record["year"] = struct.unpack("i", starter_section[3][9:13])[0]
        self.fourth_record["season"] = four_to_one(starter_section[3][13:17])
        self.fourth_record["start_year"] = struct.unpack("i", starter_section[3][17:21])[0]
        self.fourth_record["start_season"] = four_to_one(starter_section[3][21:25])
        self.fourth_record["end_year"] = struct.unpack("i", starter_section[3][25:29])[0]
        self.fourth_record["end_season"] = four_to_one(starter_section[3][29:33])
