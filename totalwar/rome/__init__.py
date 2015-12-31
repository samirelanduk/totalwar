from .file import *
from .structure import *
import datetime
import time
import shutil
import os

RTW_SAVE_LOCATION = None

def load_save(contents):
    f = SaveFile(contents)
    s = StructuredSaveFile(f)
    return s


def watch_saves(export_directory, period=60, save_names=["Autosave"]):
    """Watch a save file for changes, and make a copy when it does change."""

    if RTW_SAVE_LOCATION:
        last_time = datetime.datetime.now()

        save_names = [f + ".sav" for f in save_names if f[-4:] != ".sav"]

        while True:
            for f in os.listdir(RTW_SAVE_LOCATION):
                if f in save_names and datetime.datetime.fromtimestamp(
                  os.stat(RTW_SAVE_LOCATION + os.path.sep + f).st_mtime
                 ) > last_time:
                    #Here is a file on the watchlist which has changed
                    print("%s: copying %s" % (
                     datetime.datetime.strftime(datetime.datetime.now(), "%b-%d, %H:%M:%S"),
                     f
                    ))
                    shutil.copyfile(
                     "%s%s%s" % (RTW_SAVE_LOCATION, os.path.sep, f),
                     "%s%s%i%s" % (export_directory, os.path.sep,
                      int(datetime.datetime.now().timestamp() * 1000), f)
                    )
            last_time = datetime.datetime.now()
            time.sleep(period)

    else:
        print("You must set the RTW_SAVE_LOCATION constant first.")
