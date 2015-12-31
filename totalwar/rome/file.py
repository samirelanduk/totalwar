from .utilities import *
import math

class SaveFile(RecordContainer):
    """A representation of a RTW .sav file."""

    color = "#770101"

    def __init__(self, bytestring):

        record_starts = [index for index, _ in enumerate(bytestring)
         if index <= len(bytestring) - 4
          and four_to_one(bytestring[index:index+4]) == index]

        records = [Record(r, i) for i, r in enumerate(
         break_into_sections(bytestring, record_starts), start=1
        )]
        RecordContainer.__init__(self, records)


    def __repr__(self):
        return "<Save file: %i records, %i bytes>" % (len(self), len(self.bytestring))



class Record(BytestringContainer):
    """A top-level division of the file."""

    def __init__(self, bytestring, record_number):
        BytestringContainer.__init__(self, bytestring)

        self.number = record_number
        if self.number == 1:
            self.offset = 0
        else:
            self.offset = four_to_one(self[:4])


    def __repr__(self):
        return "<Section %i (+%i)>%s" % (self.number, self.offset, self.bytestring)
