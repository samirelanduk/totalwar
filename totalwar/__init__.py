

class SaveFile:

    def __init__(self, f):
        bytestring = f.read()

        #Get sections
        section_starts = []
        x = 0
        for index in bytestring[:-3]:
            if four_to_one(bytestring[x:x+4]) == x:
                section_starts.append(x)
            x += 1
        self.sections = break_into_sections(bytestring, section_starts)



def four_to_one(byte4):
    int32 = byte4[0] + (byte4[1] * (2**8)) + (byte4[2] * (2**16)) + (byte4[3] * (2**24))
    return int32


def break_into_sections(sequence, break_points):
    #Always start from the beginning
    if break_points[0] != 0:
        break_points = [0] + break_points

    #Get sections
    sections = []
    for index in break_points:
        if index == break_points[-1]:
            sections.append(sequence[index:])
        else:
            sections.append(sequence[index:break_points[break_points.index(index)+1]])

    return sections


def watch_saves(rtw_dir=r"C:\Program Files (x86)\Steam\steamapps\common\Rome Total War Gold\saves", new_saves=r"C:\Users\Sam\OneDrive\PROJECTS\totalwar\Saves 3"):
    import datetime
    import time
    import shutil
    import os

    #Change dir to save dir
    os.chdir(rtw_dir)

    #os.chdir(rtw_dir)
    start_time = datetime.datetime.now()

    while True:
        for f in os.listdir("."):
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
        #print("Checking again")
