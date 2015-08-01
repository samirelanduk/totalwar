from .military import Hireable
from .core import *

class City:

    def __init__(self, sections, export_descr_buildings):
        #Assign the incoming sections to the object - temporary
        self.sections = sections
        self.general_section = sections[0]
        self.name_section = sections[-1]
        if len(sections) > 3:
            self.building_sections = sections[1:-2]
            self.info_block = self.get_info_block(sections[-3])
        else:
            self.building_sections = []
            self.info_block = self.get_info_block(sections[0])

        #Get the info from the general section
        #First, parse this awful thing
        self.general1 = sections[0][:20]
        self.general2 = sections[0][20:37]
        self.general3 = sections[0][37:45]
        self.generalbuildings = []
        start = 45
        for b in range(self.general3[0]):
            if sections[0][start+1] == 0:
                self.generalbuildings.append((sections[0][start:start+50+sections[0][start]]))
                start = start+50+sections[0][start]
            else:
                self.generalbuildings.append((sections[0][start:start+52]))
                start = start + 52
        if len(self.generalbuildings) == 0:
            self.generalbuildings.append([])
        self.general5 = sections[0][start:start+4]
        self.generalunits = []
        start += 4
        for u in range(self.general5[0]):
            end = start + sections[0][start:].find(b"\xff") + 11
            self.generalunits.append(sections[0][start:end])
            start = end
        if len(self.generalunits) == 0:
            self.generalunits.append([])
        self.general7 = sections[0][start:]
        self.ID = fourToOne(self.general_section[4:8])

        #Get the name
        name_end = sections[-1][13:].find(b"\xfc") + 13
        self.name = sections[-1][13:name_end][::2].decode("UTF-8")

        #Get the location
        self.X = fourToOne(sections[0][12:16])
        self.Y = fourToOne(sections[0][16:20])

        #Get city population and happiness
        self.population = fourToOne(sections[-3][-8:-4])
        self.happiness = fourToOne(sections[-3][-4:])

        #Assign buldings
        self.buildings = [Building(x, export_descr_buildings) for x in sections[1:-2]]

        #Get the big info block
        owner_start = len(sections[-3]) - sections[-3][::-1].find(b"\xFF" * 40)
        self.info_block1 = sections[-3][owner_start:sections[-3][owner_start:].find(b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff")]
        self.info_block2 = sections[-3]
        #Determine faction ID of owner
        self.owner = fourToOne(sections[-3][owner_start:owner_start+4])
        self.owner2 = fourToOne(sections[-3][owner_start+87:owner_start+91])

        self.stack = None

        #Get info from buildings
        try:
            self.level = [x.level for x in self.buildings if x.building_type == "core_building"][0] + 1
        except(IndexError):
            #There are no core buildings here
            self.level = 0
        self.total_building_value = sum([(x.cost * (x.integrity/100.0)) for x in self.buildings])

    def get_info_block(self, section):
        block_start = len(section) - section[::-1].find(b"\xFF" * 40)
        return section[block_start:]

    def get_pre_info_block(self, section):
        ff_start = section.find(b"\xFF" * 40)
        if ff_start == -1:
            return section
        else:
            return section[:ff_start]

    def show_general(self):
        print(list(self.general1))
        print(list(self.general2))
        print(list(self.general3))
        for b in self.generalbuildings:
            print("\t" + str([x for x in b]))
        print(list(self.general5))
        for u in self.generalunits:
            print("\t" + str([x for x in u]))
        print(list(self.general7))

class Building:

    def __init__(self, section, export_descr_buildings):
        #Assign the incoming bytestring to the object - temporary
        self.bytestring = section

        #Get building info
        delim = section[6:].find(b"\x00")+6
        self.building_type = section[6:delim].decode("UTF-8")
        self.level = section[delim+5]
        culture_start = section.find(b"\xcd"*20) + 20
        self.culture = fourToOne(section[culture_start:culture_start+4])
        self.integrity = fourToOne(section[culture_start+4:culture_start+8])

        #Get info from export_descr_buildings
        building_type = [b for b in export_descr_buildings if b.name == self.building_type][0]
        level = building_type.levels[self.level]
        self.name = level.name
        self.cost = level.cost

class MercenaryRegion:

    def __init__(self, bytestring, export_descr_unit):
        self.bytestring = bytestring

        #Region name
        first_0 = bytestring.find(b"\x00")
        self.name = bytestring[:first_0].decode("UTF-8")

        #Units
        self.unit_region = bytestring[first_0+7:]
        offset = 0
        hireable_offsets = []
        while b"merc" in self.unit_region[offset:]:
            hireable_offsets.append(self.unit_region[offset:].find(b"merc") + offset)
            offset = hireable_offsets[-1] + 1
        self.hireables = []

        for x in range(len(hireable_offsets)-1):
            self.hireables.append(Hireable(self.unit_region[hireable_offsets[x]:hireable_offsets[x+1]], export_descr_unit))
        self.hireables.append(Hireable(self.unit_region[hireable_offsets[-1]:], export_descr_unit))

        #Total population
        self.population = sum([x.number * x.size for x in self.hireables])
