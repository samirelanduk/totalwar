import os
import math
import re
import struct
import json

possible_ids = {0: "romans_julii",
 1: "romans_brutii",
 2: "romans_scipii",
 3: "romans_senate",
 4: "macedon",
 5: "egypt",
 6: "seleucid",
 7: "carthage",
 8: "parthia",
 9: "pontus",
10: "gauls",
11: "germans",
12: "britons",
13: "armenia",
14: "dacia",
15: "greek_cities",
16: "numidia",
17: "scythia",
18: "spain",
19: "thrace",
20: "slave"}

prefixes = ['spanish', 'numidian', 'barb', 'eastern', 'carthaginian', 'barbarian', 'greek', 'generic', 'warband', 'cheat', 'east', 'egyptian', 'naval', 'merc', 'thracian', 'roman', 'rebel']

alphas = list(range(65,90)) + list(range(97,123)) + [39] + [32]

f = open("units.json")
unit_data = json.load(f)
f.close()

def fourToOne(l4):
    try:
        return l4[0] + (l4[1] * pow(2,8)) + (l4[2] * pow(2,16)) + (l4[3] * pow(2,24))
    except:
        print(l4)

def oneToFour(i):
    s = ("0" * (32 - len(bin(i)[2:]))) + bin(i)[2:]
    return [int(x, 2) for x in [s[:8], s[8:16], s[16:24], s[24:32]]][::-1]

class Section:
    def __init__(self, bytestring):
        self.length = len(bytestring)
        self.contents = bytestring
        self.contents_list = list(bytestring)

class Hireable:
    def __init__(self, bytestring):
        first_nul = bytestring.find(b"\x00")
        self.name = bytestring[:first_nul]
        self.contents = list(bytestring[first_nul:])

        self.experience = fourToOne(self.contents[1:5])
        self.cost = fourToOne(self.contents[5:9])
        self.replenish_min = round(struct.unpack("!f", bytearray(self.contents[9:13][::-1]))[0], 2)
        self.replenish_max = round(struct.unpack("!f", bytearray(self.contents[13:17][::-1]))[0], 2)
        self.number = self.contents[17]
        
class Mercenary_Region:
    def __init__(self, bytestring):
        #Get the region name and the remaining body
        first_nul = bytestring.find(b"\x00")
        self.name = bytestring[:first_nul].decode()
        self.contents = bytestring[first_nul:]
        self.contents_list = list(bytestring[first_nul:])

        #Get each mercenary available for sale
        mercs = [m.start() for m in re.finditer(b"merc", self.contents)]
        self.pre = list(self.contents[:mercs[0]])
        self.hireables = []
        for m in range(len(mercs) - 1):
            self.hireables.append(self.contents[mercs[m]:mercs[m+1]])
        self.hireables.append(self.contents[mercs[-1]:])
        self.hireables = [Hireable(x) for x in self.hireables]

        #The last mercenary will have the post data appended - sort this
        self.post = self.hireables[-1].contents[31:]
        self.hireables[-1].contents = self.hireables[-1].contents[:31]

class Building:
    def __init__(self, bytestring):
        self.bytestring = bytestring

        #Get base name
        name_end = bytestring[6:].find(b"\x00") + 6
        try:
            self.name = bytestring[6:name_end].decode("UTF-8")
        except:
            print(bytestring)

        #Get 'pre' block
        self.pre = list(bytestring[:6])

        #Get 'post' block
        self.post = (list(bytestring[name_end:name_end+6]))

        #Get building health
        self.health = bytestring[-20]

        #Get building 'faction'
        self.faction = bytestring[-24]

        #Get building level
        self.level = self.post[-1]
        
class City:
    #The anatomy of the city bytestring seems to be as follows:
    #   1. The 'default_set' block
    #   2. The buildings block (terminated by long ÿ)
    #   3. The unknown block (terminated by long Í)
    #   4. The name block
    def __init__(self, bytestring):
        self.bytestring = bytestring

        #Get the four blocks as bytestrings
        buildings_start = bytestring.find(b"core_building") - 6
        unknown_start = len(bytestring) - bytestring[::-1].find(b"\xFF" * 40)
        #name_start = (len(bytestring) - bytestring[::-1].find(b"\xcd" * 5))
        name_start = bytestring.find(b"\xcd" * 160) + 160
        self.default_block = bytestring[:buildings_start]
        self.buildings_block = bytestring[buildings_start:unknown_start]
        self.unknown_block = bytestring[unknown_start:name_start]
        self.name_block = bytestring[name_start:]

        #Get city name
        name_start = name_start + 25
        name = bytestring[name_start::2]
        self.name = name.decode("UTF-8")

        #Get location
        self.x = bytestring[24]
        self.y = bytestring[28]

        #Get buildings
        self.buildings = [Building(x) for x in self.buildings_block[:self.buildings_block.find(b"\xff"*100)].split(b"\xff" * 21) if len(x) > 24][:-1] #!!

        #Get 'owner' ID
        self.owner = self.unknown_block[0]

        #Get population and happiness
        self.population = fourToOne(self.name_block[:4])
        self.happiness = fourToOne(self.name_block[4:8])

class Character:
    def __init__(self, bytestring):
        f = open("names.json")
        names = json.load(f)
        f.close()
        
        self.id = fourToOne(bytestring[4:8])
        self.active_id = fourToOne(bytestring[8:12])
        self.faction_id = fourToOne(bytestring[12:16])
        self.faction = possible_ids[self.faction_id]
        self.names = [fourToOne(bytestring[20:24])]
        if bytestring[20:].find(b"\xff\xff\xff\xff") == 8:
            self.names.append(fourToOne(bytestring[24:28]))
        #if len(self.names) == 2:
        #    try:
        #        self.name = [x for x in names if x["name"] == self.faction][0]["characters"][self.names[0]] + " " + [x for x in names if x["name"] == self.faction][0]["surnames"][self.names[0]]
        #    except:
        #        print(self.faction)
        #        print(
        #else:
        #    self.name = "Unknown"

        self.unknown1 = fourToOne(bytestring[36:40])
        self.unknown2 = fourToOne(bytestring[40:44])
        self.unknown3 = fourToOne(bytestring[44:48])
        self.unknown4 = fourToOne(bytestring[48:52])
        self.unknown5 = fourToOne(bytestring[52:56])
        self.father_id = fourToOne(bytestring[56:60])
        self.spouse_id = fourToOne(bytestring[60:64])
        self.children_num = int(bytestring[64:].find(b"\xff\xff\xff\xff")/4)
        self.children = []
        for x in range(self.children_num):
            ID = fourToOne(bytestring[64+(x*4):64+((x*4)+4)])
            if ID == 0:
                self.children_num -= 1
            else:
                self.children.append(ID)
        self.command = fourToOne(bytestring[104:108])
        self.influence = fourToOne(bytestring[108:112])
        self.management = fourToOne(bytestring[112:116])
        self.subterfuge = fourToOne(bytestring[116:120])
        self.diplomacy = fourToOne(bytestring[120:124])
            
        self.contents = bytestring

class Active_Character:
    def __init__(self, lines):
        self.first_code = fourToOne(lines[0].contents[4:8])
        self.ID = fourToOne(lines[0].contents[8:12])
        self.X = fourToOne(lines[1].contents[4:8])
        self.Y = fourToOne(lines[1].contents[8:12])

class Unit:
    def __init__(self, bytestring):
        self.contents = bytestring
        name = bytestring[4:bytestring[4:].find(b"\x00") + 4]
        try:
            self.name = name.decode("UTF-8")
        except:
            self.name = name
            print("Could not decode " + str(list(name)))
        self.post_name = bytestring[bytestring[4:].find(b"\x00") + 4:]
        self.max_strength = fourToOne(self.post_name[30:34])
        self.strength = fourToOne(self.post_name[34:38])
        if self.strength <= self.max_strength:
            self.upkeep = round((self.strength / self.max_strength) * [x for x in unit_data if x["name"] == self.name][0]["upkeep"])
        else:
            self.upkeep = [x for x in unit_data if x["name"] == self.name][0]["upkeep"]
class Army:
    def __init__(self, section):
        #Find all unit names
        alphas = list(range(65,90)) + list(range(97,123)) + [39] + [32]
        offsets = []
        i = 0
        for x in section:
                if x in alphas: offsets.append(i)
                i += 1
        offsets = [x for x in offsets[:-9] if offsets[offsets.index(x)+1] == x + 1
                   and offsets[offsets.index(x)+2] == x + 2
                   and offsets[offsets.index(x)+3] == x + 3
                   and offsets[offsets.index(x)+4] == x + 4
                   and offsets[offsets.index(x)+5] == x + 5
                   and offsets[offsets.index(x)+6] == x + 6
                   and offsets[offsets.index(x)+7] == x + 7
                   and offsets[offsets.index(x)+8] == x + 8
                   and offsets[offsets.index(x)+9] == x + 9]
        offsets = [offsets[0]] + [x for x in offsets[1:] if offsets[offsets.index(x)-1] != x - 1]
        offsets = [x for x in offsets if b" " in section[x:section[x:].find(b"\x00")+x] and section[x:section[x:].find(b"\x00")+x].replace(b" ", b"").replace(b"'",b"").isalpha()]
        offsets = [x-4 for x in offsets]
        print(len(offsets))

        self.units = [section[x:offsets[offsets.index(x)+1]] for x in offsets[:-1]] + [section[offsets[-1]:]]
        self.units = [Unit(x) for x in self.units]
        self.strength = sum([x.strength for x in self.units])
        self.upkeep = sum([x.upkeep for x in self.units])
        self.contents = section
        
        
class Faction:
    def __init__(self, sections):
        self.sections = sections

        self.name = "unknown"
        for section in self.sections:
            if b"captain_card_" in section.contents:
                name_start = section.contents.find(b"captain_card_")+13
                name_end = section.contents[name_start:].find(b".tga") + name_start
                self.name = section.contents[name_start:name_end].decode("utf-8")
                break
        if self.name == "unknown":
            self.name = possible_ids[self.sections[0].contents[12]]
        if "rebel" in self.name:
            self.name = "slave"

        #Get the characters
        #self.characters = []
        #for s in self.sections:
        #    if b"data/ui" in s.contents: self.characters.append(Character(s.contents, self.name))
        self.all_characters = self.sections[:self.sections.index([x for x in self.sections if len(x.contents) == 6][0])]
        self.dup_characters = self.sections[self.sections.index([x for x in self.sections if len(x.contents) == 6][0])+1:-1]
        self.characters = [Character(x.contents) for x in self.all_characters]
        self.active_characters = [Active_Character(self.dup_characters[x*3:(x*3)+3]) for x in range(int(len(self.dup_characters)/3))]

        self.army = sections[-1]
        self.army = Army(self.army.contents)
        
class RomeSave:
    def __init__(self, bytestring):
        #Get

        #Get sections
        section_starts = [0]
        for x in range(len(bytestring) - 3):
            if fourToOne(bytestring[x:x+4]) == x: section_starts.append(x)
        sections = []
        for start in section_starts:
            if start == section_starts[-1]:
                sections.append(bytestring[start:])
            else:
                sections.append(bytestring[start:section_starts[section_starts.index(start)+1]])
        self.sections = [Section(x) for x in sections]
        
        #Assign the year
        loc = bytestring.find(b'c\x00a\x00m\x00p\x00a\x00i\x00g\x00n\x00/\x00i\x00m\x00p\x00e\x00r\x00i\x00a\x00l\x00_\x00c\x00a\x00m\x00p\x00a\x00i\x00g\x00n\x00/\x00d\x00e\x00s\x00c\x00r\x00_\x00s\x00t\x00r\x00a\x00t\x00.\x00t\x00x\x00t') + 83 + 6
        self.turn_no = bytestring[loc]
        self.year = 0 - (270 - math.floor(self.turn_no/2))
        self.season = "W" if self.turn_no % 2 else "S"

        #Get cities
        city_starts = [bytestring.find(b"default_set")]
        while bytestring[city_starts[-1]+1:].find(b"default_set") != -1:
            city_starts.append(bytestring[city_starts[-1]+1:].find(b"default_set") + 1 + city_starts[-1])

        city_ends = []
        for o in city_starts:
            end = bytestring[o:].find(b"\x00\xFC\xFC\xFC\xFC")
            city_ends.append(o + end)

        self.cities = []
        for x in range(len(city_starts)):
            self.cities.append(City(bytestring[city_starts[x]:city_ends[x]]))

        #Get mercenary regions
        regions = [b'Britain', b'Germany', b'Eastern_Europe', b'Steppes', b'Central_Europe', b'Gaul', b'Armenia', b'Cisapline_Gaul', b'Illyria', b'Thrace', b'Spain', b'Liguria', b'Northern_Greece', b'Northern_Italy', b'Persia', b'Galatia', b'Greece', b'Southern_Italy', b'Syria', b'Cilicia', b'Balearics', b'Sicily', b'North_Africa', b'Arabia', b'Sparta', b'Libya', b'Aegean', b'Egypt']
        offsets = [bytestring.find(regions[0])]
        for region in regions[1:]:
            offsets.append(bytestring[offsets[-1]:].find(region) + offsets[-1])
        self.mercenary_regions = []
        for x in range(len(offsets[:-1])):
            self.mercenary_regions.append(Mercenary_Region(bytestring[offsets[x]:offsets[x+1]]))

        #Get the last mercenary region (difficult as don't know terminal)
        offset = offsets[-1]
        mercs_in_last = bytestring[offset + len("Egypt") + 1]
        while mercs_in_last > 0:
            offset = bytestring[offset+1:].find(b"merc") + offset + 1
            mercs_in_last -= 1
        nul = bytestring[offset:].find(b"\x00") + offset
        mercend = nul + 31 + 32
        self.mercenary_regions.append(Mercenary_Region(bytestring[offsets[-1]:mercend]))

        #Get world population
        self.population = sum([x.population for x in self.cities])

        #Get the factions - armies first
        generals = [b'generals guard', b"greek general's guard", b"general's bodyguard", b"general's cavalry", b'generals cavalry', b'barb chieftain cavalry', b'barb british general', b'thracian bodyguard', b'barb scythian general', b'slave']
        armies = [self.sections.index(x) for x in self.sections if generals[0] in x.contents or generals[1] in x.contents or generals[2] in x.contents or generals[3] in x.contents or generals[4] in x.contents or generals[5] in x.contents or generals[6] in x.contents or generals[7] in x.contents or generals[8] in x.contents or generals[9] in x.contents]

        #Now find where the faction character details start
        faction_starts = []
        for section in self.sections:
            if b"data/ui" in section.contents:
                faction_starts.append(self.sections.index(section))
                break
        for army in armies[1:]:
            for section in self.sections[armies[armies.index(army)-1]:army]:
                if b"data/ui" in section.contents:
                    faction_starts.append(self.sections.index(section))
                    break

        self.factions = [self.sections[x[0]:x[1]+1] for x in zip(faction_starts, armies)]
        self.factions = [Faction(x) for x in self.factions]
                    
        
        



#Remove before publishing!
def getRecent():
    f = open(r"C:\Users\Sam\OneDrive\7) Computing\Programming\Python projects\6 -TW\Saves" + "\\" + os.listdir(r"C:\Users\Sam\OneDrive\7) Computing\Programming\Python projects\6 -TW\Saves")[-3], "rb")
    bs = f.read()
    f.close()
    return bs

recent = b""

def toFour(i):
    rep = bin(i)[2:]
    zeroes = "0" * (32 - len(rep))
    long = zeroes + rep
    four = [long[:8], long[8:16], long[16:24], long[24:32]]
    four = [int(x, 2) for x in four]
    return four
    
if __name__ == "__main__":
    recent = getRecent()
    rs = RomeSave(recent)
