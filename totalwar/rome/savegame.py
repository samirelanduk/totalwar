from .data import *
from . import lookup

class SaveGame:

    def __init__(self, structure):
        self.structured_save_file = structure

        #Process starter section
        starter_data = process_starter_section(structure.starter_section)
        self.campaign_difficulty = starter_data["campaign_difficulty"]
        self.battle_difficulty = starter_data["battle_difficulty"]
        self.faction_id = starter_data["faction_id"]
        self.faction_name = lookup.factions[self.faction_id]
        self.faction_color = lookup.faction_colors[self.faction_id]
        self.year = starter_data["year"]
        self.turn_number = starter_data["turn_number"]
