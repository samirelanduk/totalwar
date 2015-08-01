import os
import time
import shutil
import datetime

#Assumes a Steam 8.1 path
os.chdir("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Rome Total War Gold\\saves")

#Where should the saves be saved?
destination = input("Where should the saves be saved? ")

#Save name
save_name = input("Apart from autosave and quicksave, what save file should we look for? ") + ".sav"

print("")
print("Starting one minute cycles, looking at " + save_name + ", Autosave.sav and Quicksave.sav, from NOW...")
start_time = datetime.datetime.now()# - datetime.timedelta(minutes=60)

while True:
    for f in os.listdir("."):
        if (f in ["Autosave.sav", "Quicksave.sav", save_name] and
            datetime.datetime.fromtimestamp(os.stat(f).st_mtime) > start_time):
            file_name = str(datetime.datetime.now()).split(".")[0].replace(":","-") + " " + f
            print("\tCreating " + file_name)
            shutil.copyfile(f, destination + "\\" + file_name)
    start_time = datetime.datetime.now()
    time.sleep(60)
    print("Checking again...")
