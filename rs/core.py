def fourToOne(l4):
    """Take four bytes and return a 32 bit number"""
    try:
        return l4[0] + (l4[1] * pow(2,8)) + (l4[2] * pow(2,16)) + (l4[3] * pow(2,24))
    except:
        print(l4)

def oneToFour(i):
    """Take a 32 bit number and return 4 bytes"""
    s = ("0" * (32 - len(bin(i)[2:]))) + bin(i)[2:]
    return [int(x, 2) for x in [s[:8], s[8:16], s[16:24], s[24:32]]][::-1]

def findFirstNot(bytestring, char):
    """Takes a bytestring and returns the index of the first character that isn't char"""
    x = 0
    for b in bytestring:
        if type(char) == type(0):
            if b != char:
                return x
        else:
            if b not in char:
                return x
        x += 1
    return x

def breakIntoSections(sequence, break_points):
    """Takes a generic sequence and breaks it into sections based on indeces provided"""

    #Always start from the beginning
    if break_points[0] != 0:
        break_points = [0] + break_points

    sections = []
    for index in break_points:
        if index == break_points[-1]:
            sections.append(sequence[index:])
        else:
            sections.append(sequence[index:break_points[break_points.index(index)+1]])

    return sections
