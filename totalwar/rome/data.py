from .utilities import *
import struct

def process_starter_section(starter_section):
    data = {}

    data["campaign_difficulty"] = four_to_one(starter_section[0][584:588])
    data["battle_difficulty"] = four_to_one(starter_section[0][588:592])
    data["faction_id"] = starter_section[0][1273]
    data["year"] = struct.unpack("i", starter_section[0][1276:1280])[0]

    data["turn_number"] = four_to_one(starter_section[3][5:9])

    return data
