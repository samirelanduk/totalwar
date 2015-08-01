from .core import *
import struct
import re
from .core import *



def is_delim(bytestring):
    delim = True
    pos = 0
    for char in bytestring:
        if char == 1 or char == 2 or char == 3 or char == 255 or (char == 0 and pos != 0 and pos != len(bytestring)-1):
            pass
        else:
            delim = False
            break
        pos += 1
    return delim

def is_stack_start(subsection):
    if subsection[0] == 0 and subsection[1] == 0 and subsection[3] == 0:
        return False
    else:
        return True

def get_ff_end(bytestring, start):
    bytestring = bytestring[start:]
    x = 0
    for char in bytestring:
        if char != 255:
            return x + start
        x += 1
    return x + start

class Hireable:

    def __init__(self, bytestring, export_descr_unit):
        self.bytestring = bytestring

        #Name and trailing data
        first_0 = bytestring.find(b"\x00")
        self.name = bytestring[:first_0].decode("UTF-8")
        self.data = bytestring[first_0+1:first_0+31]

        self.experience = fourToOne(self.data[0:4])
        self.cost = fourToOne(self.data[4:8])
        self.replenish_min = round(struct.unpack("!f", bytearray(self.data[8:12][::-1]))[0], 2)
        self.replenish_max = round(struct.unpack("!f", bytearray(self.data[12:16][::-1]))[0], 2)
        self.number = fourToOne(self.data[16:20])

        #Get number of soldiers in the unit_region
        unit = [x for x in export_descr_unit if x.dictionary["type"] == self.name][0]
        self.size = int(unit.dictionary["soldier"].split(", ")[1]) * unit.multiplier


class Army:

    def __init__(self, section, export_descr_unit):
        self.bytestring = section

        self.prelim = section[:6]
        self.units_bytestring = section[6:]
        self.subsections = []

        self.break_into_subsections()

        #Divide army into stacks
        stack_starts = []
        x = 0
        for subsection in self.subsections:
            if is_stack_start(subsection):
                stack_starts.append(x)
            x += 1
        self.stacks = []
        for x in range(len(stack_starts)-1):
            self.stacks.append(Stack(self.subsections[stack_starts[x]:stack_starts[x+1]], export_descr_unit))
        self.stacks.append(Stack(self.subsections[stack_starts[-1]:], export_descr_unit))

        self.strength = 69# sum([x.strength for x in self.stacks])
        self.faction_ID = self.stacks[0].faction_ID
        self.upkeep = sum([x.upkeep for x in self.stacks])

    def break_into_subsections(self):
        #Takes units_bytestring and assigns strings to subsections from it
        self.subsections = []

        #Get the start of all ff blocks, however small
        starts = []
        x = 0
        for char in self.units_bytestring:
            if char == 255:
                starts.append(x)
            x += 1
        starts = [x for x in starts if starts[starts.index(x)-1] != 255]

        #Get the ends of all these strings
        ends = [get_ff_end(self.units_bytestring, x) for x in starts]

        #Get a list of ff starts and ends, and remove single ffs
        ffs = list(zip(starts, ends))
        ffs = [list(x) for x in ffs if x[0] != x[1]]

        remove = []
        x = len(ffs) - 1
        while x > 0:
            #Does this block start less than 4 bytes after the end of the previous one?
            if ffs[x][0] <= ffs[x-1][1] + 4:
                #Yes
                ffs[x-1][1] = ffs[x][1]
                remove.append(x)
            x -= 1

        #Remove some ff strings
        ffs = [x for x in ffs if ffs.index(x) not in remove and x[1] - x[0] > 6]

        self.subsections.append(self.units_bytestring[:ffs[0][0]])


class Stack:

    def __init__(self, subsections, export_descr_unit):
        self.subsections = subsections
        self.stackbytes = None

        self.slice_off_stackbytes()

        self.ID = fourToOne(self.stackbytes[:4])
        #self.cityID = fourToOne(self.stackbytes[second_ff+12:second_ff+16])
        self.cityID = 69

        self.units = [Unit(subsections[0], export_descr_unit)]
        for subsection in subsections[1:-1]:
            self.units.append(Unit(subsection, export_descr_unit))

        self.strength = sum([x.strength for x in self.units])
        self.faction_ID = self.units[0].faction_ID
        self.upkeep = sum([x.upkeep for x in self.units])

    def slice_off_stackbytes(self):
        """Takes the first subsection, finds where the first unit begins, and extracts the bit before it as a stack-wide property"""

        for char in range(len(self.subsections[0])):
            next_space = self.subsections[0][char:].find(b" ") + char
            if self.subsections[0][char:next_space] in [b'egyptian', b'greek', b'thracian', b'cheat', b'roman', b'spanish', b'merc', b'carthaginian', b'generic', b'naval', b'barb', b'barbarian', b'numidian', b'eastern', b'warband', b'east', b'rebel']:
                self.stackbytes = self.subsections[0][:char]
                self.subsections[0] = self.subsections[0][char:]
                return
        print("Didn't find unit start - " + str(fourToOne(self.subsections[0][:4])))
        print(self.subsections)


class Unit:

    def __init__(self, bytestring, export_descr_unit):
        self.bytestring = bytestring

        while bytestring[0] < 65 or bytestring[1] < 65 or bytestring[2] < 65 or bytestring[3] < 65:
            bytestring = bytestring[4:]

        first_0 = bytestring.find(b"\x00")
        try:
            self.name = bytestring[:first_0].decode("UTF-8")
        except:
            print("!")
            self.name = bytestring[:first_0]
        self.post_name = bytestring[first_0:]

        self.faction_ID = self.post_name[1]
        self.max_strength = fourToOne(self.post_name[30:34])
        self.strength = fourToOne(self.post_name[34:38])

        try:
            unit = [x for x in export_descr_unit if x.dictionary["type"] == self.name][0]
            self.cost = int(unit.dictionary["stat_cost"].split(", ")[1])
            self.max_upkeep = int(unit.dictionary["stat_cost"].split(", ")[2])
            if self.max_strength == self.strength:
                self.upkeep = self.max_upkeep
            else:
                self.upkeep = round((float(self.strength)/self.max_strength) * self.max_upkeep)
        except:
            self.cost, self.nax_upkeep, self.upkeep = 0,0,0
            try:
                print("Couldn't find " + str(self.name))
            except:
                print("Couldn't find bytes")
