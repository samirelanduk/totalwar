from .utilities import *
import quickplots

class StructuredSaveFile:
    """A sav file with sections identiifed."""

    def __init__(self, save_file):
        self.save_file = save_file

        for record in self.save_file:
            record.section = None

        self.starter_section = StarterSection(self.save_file)
        self.step_section = StepSection(self.save_file)
        self.cities_section = CitiesSection(self.save_file)
        self.military_section = MilitarySection(self.save_file)
        self.unused_records = RecordContainer(
         [r for r in save_file if not r.section]
        )
        self.chart = quickplots.MultiSeriesAxisChart(
         (self.starter_section.get_records_chart(),
         self.step_section.get_records_chart(),
         self.cities_section.get_records_chart(),
         self.military_section.get_records_chart())
        )



class Section(RecordContainer):

    def __init__(self):
        for record in self.records:
            record.section = self



class StarterSection(Section):

    color = "#111177"

    def __init__(self, save_file):
        for i, record in enumerate(save_file):
            if b"mausoleum" in record:
                RecordContainer.__init__(self, save_file[:i+1])
                break
        Section.__init__(self)



class StepSection(Section):

    color = "#117711"

    def __init__(self, save_file):
        for i, record in enumerate([r for r in save_file if not r.section]):
            if len(record) > 10000:
                RecordContainer.__init__(self, [r for r in save_file if not r.section][:i])
                break
        Section.__init__(self)




class CitiesSection(Section):

    color = "#CCCC99"

    def __init__(self, save_file):
        for i, record in enumerate([r for r in save_file if not r.section]):
            if b"Eastern_Europe" in record:
                RecordContainer.__init__(self, [r for r in save_file if not r.section][:i+1])
                break
        Section.__init__(self)



class MilitarySection(Section):

    color = "#AA7777"

    def __init__(self, save_file):
        RecordContainer.__init__(self, [r for r in save_file if not r.section])
        Section.__init__(self)
