import math
import os
from .locations import City, MercenaryRegion
from .military import Army
from .core import *


class RomeSave:
    """Representation of a Rome: Total War .sav file"""
    def __init__(self, bytestring):
        #Assign the incoming bytestring to the object - this is temporary for testing
        self.bytestring = bytestring

        #Break bytestring into sections
        section_starts = []
        for x in range(len(bytestring) - 3):
            if fourToOne(bytestring[x:x+4]) == x: section_starts.append(x)
        self.sections = breakIntoSections(bytestring, section_starts)
        self.sections = [Section(self.sections[0], first=True)] + [Section(x) for x in self.sections[1:]]
        for section in self.sections:
            section.index = self.sections.index(section)

        #Identify known sections
        self.sections_dict = {}
        self.find_sections()

        #Get year information
        year_section = self.sections[self.sections_dict["year-s"]].bytestring
        self.turn_no = fourToOne(year_section[5:9])

        #Get cities
        cities_sections = [self.sections[x] for x in self.sections_dict["cities-s"]]
        city_starts = [cities_sections.index(x) + 2 for x in cities_sections[:-2] if len(x.bytestring) == 4]
        self.cities = breakIntoSections(cities_sections, city_starts)


        #Get RTW file information
        #f = open("export_descr_unit.txt")
        #lines = [x for x in f.readlines() if  len(x.rstrip()) > 0 and x[0] != ";"]
        #f.close()
        #unit_starts = [lines.index(x) for x in lines if x[:4] == "type"]
        #self.export_descr_unit = [eduUnit(lines[x:unit_starts[unit_starts.index(x)+1]]) for x in unit_starts[:-1]]
        #self.export_descr_unit.append(eduUnit(lines[unit_starts[-1]:]))
#
        #Get global information from all cities
        #self.civilian_population = sum([x.population for x in self.cities])
        #self.average_happiness = sum([x.happiness * x.population for x in self.cities]) / self.civilian_population
        #self.total_city_value = sum([x.total_building_value for x in self.cities])

        #Get mercenary regions
        #regions = [b'Britain', b'Germany', b'Eastern_Europe', b'Steppes', b'Central_Europe', b'Gaul', b'Armenia', b'Cisapline_Gaul', b'Illyria', b'Thrace', b'Spain', b'Liguria', b'Northern_Greece', b'Northern_Italy', b'Persia', b'Galatia', b'Greece', b'Southern_Italy', b'Syria', b'Cilicia', b'Balearics', b'Sicily', b'North_Africa', b'Arabia', b'Sparta', b'Libya', b'Aegean', b'Egypt']
        #mercenary_section = self.cities[-1].sections[-1]
        #mercenary_offsets = [mercenary_section.find(regions[0])]
        #for region in regions[1:]:
        #    mercenary_offsets.append(mercenary_section[mercenary_offsets[-1]:].find(region) + mercenary_offsets[-1])
        #self.mercenary_regions = []
        #for x in range(len(mercenary_offsets)-1):
        #    self.mercenary_regions.append(MercenaryRegion(mercenary_section[mercenary_offsets[x]:mercenary_offsets[x+1]], self.export_descr_unit))
        #self.mercenary_regions.append(MercenaryRegion(mercenary_section[mercenary_offsets[-1]:], self.export_descr_unit))

        #Get info from all mercenary regions
        #self.mercenary_population = sum([x.population for x in self.mercenary_regions])

        #Get the armies
        #generals = [b'generals guard', b"greek general's guard", b"general's bodyguard", b"general's cavalry", b'generals cavalry', b'barb chieftain cavalry', b'barb british general', b'thracian bodyguard', b'barb scythian general', b'slave']
        #army_sections = [self.sections.index(x) for x in self.sections if generals[0] in x or generals[1] in x or generals[2] in x or generals[3] in x or generals[4] in x or generals[5] in x or generals[6] in x or generals[7] in x or generals[8] in x or generals[9] in x]
        #army_sections = [self.sections[x] for x in army_sections]
        #army_sections = tape_broken_armies(self.sections, army_sections)
        #self.armies = [Army(x, self.export_descr_unit) for x in army_sections]

        #Get info from all armies
        #self.enlisted_population = sum([x.strength for x in self.armies])

        #Assign stacks to cities
        #for army in self.armies:
        #    for stack in army.stacks:
        #        for city in self.cities:
        #            if city.ID == stack.cityID:
        #                city.stack = stack
        #                break

#    def get_city_by_name(self, name):#
#        try:
#            return [x for x in self.cities if x.name == name][0]
#        except:
#            return None

#I hate that I even need this function
#def tape_broken_armies(all_sections, army_sections):
    #Find out which army sections are in fact the second halves of other armies
#    brokens = []
#    for army in army_sections[1:]:
#        army_index_all = all_sections.index(army)
#        army_index_armies = army_sections.index(army)
#        previous_index_all = all_sections.index(army_sections[army_index_armies-1])
#        if army_index_all == previous_index_all + 1:
#            brokens.append(army_index_armies)

    #Reuinite them with their other halves
#    for broke in brokens:
#        army_sections[broke-1] += army_sections[broke]
#
    #Remove the second halves
#    army_sections = [x for x in army_sections if army_sections.index(x) not in brokens]
#    return army_sections

    def find_sections(self):
        """Allocates values sections_dict by looking through all sections"""
        self.sections_dict["year-s"] = 3

        #Cities
        cities_start = 0
        for section in self.sections:
            if b"default" in section.bytestring:
                cities_start = self.sections.index(section) + 1
                break
        cities_end = 0
        for section in self.sections[cities_start:]:
            if b"Eastern_Europe" in section.bytestring:
                cities_end = self.sections.index(section) + 1
                break
        self.sections_dict["cities-s"] = list(range(cities_start, cities_end))


class Section:

    def __init__(self, bytestring, first=False):
        self.bytestring = bytestring
        self.offset = fourToOne(bytestring[:4]) if not first else 0
        self.contents = bytestring[4:] if not first else bytestring

    def __repr__(self):
        return str(self.offset) + ": " + str(list(self.contents))


class edbBuilding:

    def __init__(self, lines):
        self.lines = lines

        #Get name
        self.name = lines[0].split()[1].rstrip()

        #Assign levels
        levels = [line for line in lines if line.lstrip()[:7] == "levels "][0].split()[1:]
        self.levels = []
        for level in levels[:-1]:
            level_start = lines.index([line for line in lines if line[:len(level) + 8] == " "*8 + level][0])
            level_end = lines.index([line for line in lines if line[:len(levels[levels.index(level)+1])+8] == " "*8 + levels[levels.index(level)+1]][0])
            self.levels.append(edbLevel(lines[level_start:level_end]))
        last_level_start = lines.index([line for line in lines if line[:len(levels[-1]) + 8] == " "*8 + levels[-1]][0])
        last_level_end = [lines.index(line) for line in lines[last_level_start:] if line[:5] == "    }"][0]
        self.levels.append(edbLevel(lines[last_level_start:last_level_end]))


class edbLevel:

    def __init__(self, lines):
        self.lines = lines

        #Get name
        self.name = lines[0].lstrip().split()[0]

        #Get cultures which can build it. Some don't list factions, so in that case just assign nothing here
        try:
            self.cultures = lines[0].split("factions { ")[1].rstrip()[:-3].split(", ")
        except:
            self.cultures = []

        #Get cost
        self.cost = int([line for line in lines if line.lstrip()[:4] == "cost"][0].split("cost ")[1].rstrip())


class eduUnit:
    def __init__(self, lines):
        self.lines = lines

        self.dictionary = {}
        for line in lines:
            key = line.split()[0]
            value = line[len(key):].lstrip().rstrip()
            self.dictionary[key] = value
        self.multiplier = 4 #HARD CODED - FIX!



def watch_saves(rtw_dir=r"C:\Program Files (x86)\Steam\steamapps\common\Rome Total War Gold\saves", new_saves=r"C:\Users\Sam\OneDrive\7) Computing\Programming\Python projects\6 -TW\Saves 2"):
    import datetime
    import time
    import shutil

    #os.chdir(rtw_dir)
    start_time = datetime.datetime.now()

    while True:
        for f in os.listdir(rtw_dir):
            if "000.sav" not in os.listdir(new_saves) and f == "Quicksave.sav" and datetime.datetime.fromtimestamp(os.stat(f).st_mtime) > start_time:
                #Grab the very first shot
                print("Saving first at " + str(start_time))
                shutil.copyfile(rtw_dir +"\\" + f, new_saves + "\\000.sav")
            if f == "Autosave.sav" and datetime.datetime.fromtimestamp(os.stat(rtw_dir +"\\" + f).st_mtime) > start_time:
                #There is a new autosave to harvest
                print("Saving at " + str(start_time))
                shutil.copyfile(rtw_dir +"\\" + f, new_saves + "\\" + str(datetime.datetime.now()).split(".")[0].replace(":","-") + ".sav")

        start_time = datetime.datetime.now()
        time.sleep(1)
        print("Checking again")

def load_saves(directory = r"C:\Users\Sam\OneDrive\7) Computing\Programming\Python projects\6 -TW\Saves 2"):
    import matplotlib.pyplot as plt

    big = []
    savs = [x for x in os.listdir(directory) if ".sav" in x]
    for sav in savs[:2]:
        print(sav)
        f = open(directory + "\\" + sav, "rb")
        big.append(RomeSave(f.read()))
        f.close()
        print("")

    sections_per_file = plt.figure()
    sections_per_file.add_subplot(111)
    file_no = [str(big.index(x) + 1) for x in big]
    section_no = [len(x.sections) for x in big]
    sections_per_file.axes[0].bar(file_no, section_no)
    sections_per_file.axes[0].axis([0,3,0,3000])
    sections_per_file.show()



    return big





#Get global representations of export_descr_unit and export_descr_buildings
my_dir = __file__[:0-__file__[::-1].find("\\")]
f = open(my_dir + "export_descr_buildings.txt")
lines = [x for x in f.readlines() if len(x) > 0 and x[0] != ";"]
while lines[0][:8] != "building":
    lines = lines[1:]
f.close()
building_starts = [lines.index(x) for x in lines if x[:8] == "building"]
export_descr_buildings = [edbBuilding(x) for x in breakIntoSections(lines, building_starts)]
