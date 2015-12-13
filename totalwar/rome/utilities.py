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
