import os
from sav import RomeSave

os.chdir(r"C:\Users\Sam\OneDrive\7) Computing\Programming\Python projects\6 -TW\Saves")

big = []
for f in os.listdir("."):
    if "Autosave" in f:
        b = open(f, "rb")
        big.append(RomeSave(b.read()))
        b.close()
