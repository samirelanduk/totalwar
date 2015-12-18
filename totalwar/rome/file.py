from .utilities import *
import quickplots
import math

class RecordContainer:
    """Any object which contains a list of records."""

    def __init__(self, records):
        self.records = records


    def __len__(self):
        return len(self.records)


    def __getitem__(self, key):
        return self.records[key]


    def get_records_chart(self, log=None, start=None, end=None):
        data = [(r.number, len(r.bytestring)) for r in self[start:end]]
        if log:
            data = [(d[0], math.log(d[1])) for d in data]
        edge_width = 1 if len(data) < 100 else 0
        bar_width = 0.8 if len(data) < 100 else 0
        color = "#770101"
        chart = quickplots.BarChart(data,
         edge_width=edge_width, bar_width=bar_width, color=color,
          x_limit=[data[0][0]-0.5, data[-1][0]+0.5], x_label="Record number",
           x_ticks=[data[0][0], data[-1][0]],title="Record lengths in save file")
        return chart


    def get_record_by_number(self, number):
        for record in self:
            if record.number == number:
                return record



class BytestringContainer:
    """Any object which contains a bytestring."""

    def __init__(self, bytestring):
        self.bytestring = bytestring


    def __len__(self):
        return len(self.bytestring)


    def __getitem__(self, key):
        return self.bytestring[key]


    def as_list(self):
        return list(self.bytestring)


    def as_string(self):
        chars = [chr(b) if (b > 64 and b <91) or (b > 96 and b < 123) else "."
         for b in self.bytestring]
        return "".join(chars)


    def get_byte_trend_chart(self, byte=0):
        chart = quickplots.SingleSeriesAxisChart(
         [(i, (b == byte)) for i,b in enumerate(self.bytestring, start=1)]
        ).generate_moving_average(
         n = math.ceil(len(self.bytestring) / 50)
        )
        chart.line_width = 1
        return chart




class SaveFile(RecordContainer, BytestringContainer):
    """A representation of a RTW .sav file."""

    def __init__(self, bytestring):
        BytestringContainer.__init__(self, bytestring)

        record_starts = [index for index, _ in enumerate(self.bytestring)
         if index <= len(self.bytestring) - 4
          and four_to_one(self.bytestring[index:index+4]) == index]

        records = [Record(r, i) for i, r in enumerate(
         break_into_sections(self.bytestring, record_starts), start=1
        )]
        RecordContainer.__init__(self, records)


    def __repr__(self):
        return "<Save file: %i records, %i bytes>" % (len(self), len(self.contents))


    def __contains__(self, key):
        return key in self.bytestring



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
