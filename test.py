#This is a private module for cd-ing to a savefile directory

import os
os.chdir(r"C:\Users\Sam\OneDrive\7) Computing\Programming\Python projects\6 -TW\Saves 2")

fileno = int(input("File no: "))
f = open([x for x in os.listdir(".") if "." in x][fileno], "rb")
data = f.read()
f.close()

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

import rs
from rs import RomeSave
sav = RomeSave(data)
