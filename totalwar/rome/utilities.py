import sys
sys.path = ["/Users/sam/Dropbox/PROJECTS/quickplots"] + sys.path
import quickplots
import math
from collections import Counter

class BytestringContainer:
    """Any object which contains a bytestring."""

    def __init__(self, bytestring):
        self.bytestring = bytestring


    def __len__(self):
        return len(self.bytestring)


    def __getitem__(self, key):
        return self.bytestring[key]


    def __contains__(self, key):
        return key in self.bytestring


    def as_list(self):
        return list(self.bytestring)


    def as_string(self):
        chars = [chr(b) if chr(b).isalpha() and b < 128 else "." if b else " "
         for b in self.bytestring]
        return "".join(chars)


    def compare(self, other):
        if len(other) != len(self):
            print("Lengths do not match.")
        else:
            for i, pair in enumerate(zip(self, other), start=1):
                if pair[0] != pair[1]:
                    print("%i: %i, %i" % (i, pair[0], pair[1]))


    def rank_subbytes(self, length=4):
        subbytes = []
        for frame in range(length):
            for start, _ in enumerate(self.bytestring[frame:]):
                try:
                    subbytes.append(self.bytestring[frame:][start: start + 4])
                    #print(subbytes[-1])
                except IndexError:
                    pass
        subbytes = [s for s in subbytes if len(s) == 4]
        return Counter(subbytes)


    def split_on_substring(self, substring):
        length = len(substring)
        bytestrings = []
        bytestring = bytearray()
        for index, b in enumerate(self.bytestring[:0-length]):
            if self.bytestring[index:index+length] == substring:
                bytestrings.append(BytestringContainer(bytes(bytestring)))
                bytestring = bytearray()
            bytestring.append(b)
        return bytestrings




    def get_byte_trend_chart(self, byte=0):
        chart = quickplots.SingleSeriesAxisChart(
         [(i, (b == byte)) for i,b in enumerate(self.bytestring, start=1)]
        ).generate_moving_average(
         n = math.ceil(len(self.bytestring) / 50)
        )
        chart.width = 1
        return chart



class RecordContainer(BytestringContainer):
    """Any object which contains a list of records."""

    color = "#999999"

    def __init__(self, records):
        self.records = records
        byteslist = []
        for record in self.records:
            byteslist += record.as_list()
        BytestringContainer.__init__(self, bytes(byteslist))


    def __len__(self):
        return len(self.records)


    def __getitem__(self, key):
        return self.records[key]


    def __contains__(self, key):
        return key in self.records


    def get_records_chart(self, log=None, start=None, end=None):
        data = [(r.number, len(r.bytestring)) for r in self[start:end]]
        if log:
            data = [(d[0], math.log(d[1])) for d in data]
        edge_width = 1 if len(data) < 100 else 0
        bar_width = 0.8 if len(data) < 100 else 1
        chart = quickplots.BarChart(data,
         edge_width=edge_width, bar_width=bar_width, color=self.color,
          x_limit=[data[0][0]-0.5, data[-1][0]+0.5], x_label="Record number",
           x_ticks=[data[0][0], data[-1][0]], xgrid = False,
            title="Record lengths in save file")
        return chart


    def get_record_by_number(self, number):
        for record in self:
            if record.number == number:
                return record




def four_to_one(*the_bytes):
    """Takes four bytes and returns a 32 bit integer."""

    if len(the_bytes) == 1:
        the_bytes = the_bytes[0]

    return the_bytes[0] +\
     (the_bytes[1] * pow(2,8)) +\
      (the_bytes[2] * pow(2,16)) +\
       (the_bytes[3] * pow(2,24))


def break_into_sections(sequence, break_points):
    """Takes a generic sequence and breaks it into sections based on indeces provided"""

    #Always start from the beginning
    if break_points[0] != 0:
        break_points = [0] + break_points

    sections = []
    for index, bp in enumerate(break_points):
        if index == len(break_points) - 1:
            sections.append(sequence[bp:])
        else:
            sections.append(sequence[bp:break_points[index + 1]])

    return sections
