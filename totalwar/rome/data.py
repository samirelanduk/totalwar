from .utilities import *
import struct

class DataSaveFile:

    def __init__(self, structured_save_file):
        self.structured_save_file = structured_save_file

        self.starter_section = DataStarterSection(self.structured_save_file.starter_section)



class DataStarterSection:
    def __init__(self, starter_section):
        self.first_record = {}

        self.first_record["campaign_difficulty"] = four_to_one(starter_section[0][584:588])
        self.first_record["battle_difficulty"] = four_to_one(starter_section[0][588:592])
        self.first_record["faction_id"] = starter_section[0][1273]
        self.first_record["year"] = struct.unpack("i", starter_section[0][1276:1280])[0]

        #data["turn_number"] = four_to_one(starter_section[3][5:9])
