from .data import *
from . import lookup

class SaveGame:

    def __init__(self, data_save_file):
        self.data_save_file = data_save_file

        #Process starter section
        self.campaign_difficulty = self.data_save_file.starter_section.first_record["campaign_difficulty"]
        self.battle_difficulty = self.data_save_file.starter_section.first_record["battle_difficulty"]
        self.faction_id = self.data_save_file.starter_section.first_record["faction_id"]
        self.faction_name = lookup.factions[self.faction_id]
        self.faction_color = lookup.faction_colors[self.faction_id]
        self.year = self.data_save_file.starter_section.first_record["year"]
        #self.turn_number = self.data_save_file.starter_section.first_record["turn_number"]
