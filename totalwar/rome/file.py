from .utilities import *

class SaveFile:
    """A representation of a RTW .sav file."""

    def __init__(self, bytestring):
        self.contents = bytestring

        section_starts = [index for index, _ in enumerate(self.contents)
         if index <= len(self.contents) - 4
          and four_to_one(self.contents[index:index+4]) == index]
        self.sections = [Section(s, i) for i, s in enumerate(
         break_into_sections(self.contents, section_starts), start=1
        )]


    def __repr__(self):
        return "<Save file: %i sections, %i bytes>" % (len(self.sections), len(self.contents))




class Section:
    """A top-level division of the file."""

    def __init__(self, bytestring, section_number):
        self.bytestring = bytestring
        self.section_number = section_number
        if self.section_number == 1:
            self.offset = 0
        else:
            self.offset = four_to_one(self.bytestring[:4])


    def __repr__(self):
        return "<Section %i (+%i)>%s" % (self.section_number, self.offset, self.bytestring)
