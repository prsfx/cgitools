# -*- coding: utf-8 -*-

print("\nprsfxTools first base module...\n")

import os
import sys
import platform
import getpass

try:
    import maya.mel as mel
    import maya.cmds as cmds
    isMaya = True
except ImportError:
    isMaya = False


CheckPyVer  = sys.version
CheckOS     = platform.system()
CheckUser   = getpass.getuser()
MayaVer     = int(cmds.about(api=True))


def MayaApiVersion():
    return int(cmds.about(api=True))


if MayaApiVersion() < 20170000:
    print("\nWarning: This version is not supported.")
    print("Your version: " + str(MayaVer) + "\n")

# elif MayaApiVersion() >= 2017300 and MayaApiVersion() != 2020500:
elif MayaApiVersion() <= 20200500:
    from py27 import artistplayblast
    reload(artistplayblast)
    artistplayblast.main()

elif MayaApiVersion() > 20200500:
    print("\nIt's about time to use Python 3?")
    print("Your version: " + str(MayaVer) + "\n")

else:
    print("This is absurd.\n")

