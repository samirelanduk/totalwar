from .utilities import *
import struct

class DataSaveFile:

    def __init__(self, structured_save_file):
        self.structured_save_file = structured_save_file

        self.starter_section = DataStarterSection(self.structured_save_file.starter_section)
        self.cities_section = DataCitiesSection(self.structured_save_file.cities_section)



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



class DataCitiesSection:
    def __init__(self, cities_section):
        #Split the records up
        self.city_bytestrings = cities_section.split_on_substring(b"\x0c\x00default_set")
        self.cities = [self.process_city_bytestring(c) for c in self.city_bytestrings[1:]]


    def process_city_bytestring(self, city_bytestring):
        city = {}
        loc = 0

        #Process INFO bytes
        length = city_bytestring[loc]
        city["set"] = city_bytestring[loc+2:loc+length+1]
        loc += length + 2
        loc += 4 #Skip record offset
        city["city_id"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 8 #Also skip 252 252 252 252
        city["x"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 4
        city["y"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 4
        city["unknown1"] = city_bytestring[loc:loc+17]
        loc += 17

        #Process CONSTRUCTION bytes
        city["construction_num"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 4
        city["unknown2"] = city_bytestring[loc:loc+4]
        loc += 4
        city["constructions"] = []
        for _ in range(city["construction_num"]):
            if city_bytestring[loc + 1] == 0 and city_bytestring[loc] < 20:
                ##This construction sequence contains the name of the building
                city["constructions"].append(city_bytestring[loc:loc+50+city_bytestring[loc]])
                loc += (50 + city_bytestring[loc])
            else:
                #This construction sequence uses a building ID as identifier
                city["constructions"].append(city_bytestring[loc:loc+52])
                loc += 52

        #Process TRAINING bytes
        city["training_num"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 4
        city["trainings"] = []
        for _ in range(city["training_num"]):
            end = city_bytestring[loc:].find(b"\xff") + 11 + loc
            city["trainings"].append(city_bytestring[loc:end])
            loc = end
        city["unknown3"] = city_bytestring[loc:loc+4]
        loc += 4

        #Process BUILDINGS bytes
        city["building_num"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 4
        city["buildings"] = []
        for _ in range(city["building_num"]):
            building = {}
            loc += 4 #Skip record offset
            building["type_length"] = city_bytestring[loc]
            loc += 2
            building["type"] = city_bytestring[loc:loc+building["type_length"]-1]
            loc += building["type_length"]
            building["building_id"] = four_to_one(city_bytestring[loc:loc+4])
            loc += 4
            building["level"] = city_bytestring[loc]
            loc += 1
            loc += 20 #Skip \xcd x 20
            building["culture_id"] = four_to_one(city_bytestring[loc:loc+4])
            loc += 4
            building["health"] = four_to_one(city_bytestring[loc:loc+4])
            loc += 4
            building["unknown1"] = city_bytestring[loc]
            loc += 1
            loc += 3 #Skip \xcd\xcd\xcd
            building["unknown2"] = city_bytestring[loc:loc+12]
            loc += 12
            loc += 21 #Skip \xff * 21
            city["buildings"].append(building)

        #Process POSTF bytes
        while city_bytestring[loc] == 255:
            loc += 1
        delimstart = city_bytestring[loc:].find(b'\xff' * 8)
        city["unknown4"] = city_bytestring[loc:loc+delimstart]
        loc += delimstart
        while city_bytestring[loc] == 255:
            loc += 1
        delimstart = city_bytestring[loc:].find(b'\xcd' * 8)
        city["unknown4"] = city_bytestring[loc:loc+delimstart]
        loc += delimstart
        while city_bytestring[loc] == 205:
            loc += 1
        city["population"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 4
        city["happiness"] = four_to_one(city_bytestring[loc:loc+4])
        loc += 4

        #Process NAME bytes
        loc += 4 #Skip record offset
        city["unknown5"] = city_bytestring[loc:loc+11]
        loc += 11
        city["name_length"] = city_bytestring[loc]
        loc += 2
        city["name"] = city_bytestring[loc:loc+(city["name_length"]*2)][::2]
        loc += city["name_length"] * 2





        city["next"] = city_bytestring[loc:loc+5]
        return city
