# -*- coding: utf-8 -*-

import os
import sys
import platform
import getpass


try:
    import maya.mel as mel
    import maya.cmds as cmds
    isMaya = True
    print("configure for Maya")
except ImportError:
    isMaya = False
    print("fail to configure for Maya")


tool_name = "Artist Playblast"


Ver = int(cmds.about(api=True))
CheckOS = platform.system()
CheckUser = getpass.getuser()
CheckPyVer = sys.version



print("")
print("Maya Version : " + str(Ver))
print("OS           : " + CheckOS)
print("User         : " + CheckUser)
print("Py Version   : " + CheckPyVer)
print("")




# 
def MayaApiVersion():
    return int(cmds.about(api=True))


# 
def onMayaDroppedPythonFile(*args, **kwargs):
    """ this function available since Maya 2017.3 """
    pass


# 
def onMayaDropped():

    # 
    if MayaApiVersion() < 2017300:
        print("WARNING: This version is not supported. Your Maya version: " + Ver)


    # 
    # elif MayaApiVersion() >= 2017300 and MayaApiVersion() != 2020500:
    elif MayaApiVersion() <= 20200500:
        """ Artist Playblast tools setup """
        SourcePath = os.path.join(os.path.dirname(__file__))
        artistplayblast_icon = os.path.join(SourcePath, "py27/icons", "artistplayblast-icon.png") # locate the icon
        # artistplayblast_icon = os.path.join(os.getcwd(), "/icons/artistplayblast-icon.png") # locate the icon

        SourcePath = os.path.normpath(SourcePath)
        artistplayblast_icon = os.path.normpath(artistplayblast_icon)

        # 
        if not os.path.exists(artistplayblast_icon):
            raise IOError("Can't find " + artistplayblast_icon)

        # 
        for path in sys.path:
            if os.path.exists(path + "/py27/__init__.py"):
                print("Finished")

        # 
        artistplayblast_command = """
# Artist Playblast
# MIT License
# (c) Prana Ronita

import os
import sys

if not os.path.exists(r'{path}'):
    raise IOError(r'The source path "{path}" does not exists.')

if r'{path}' not in sys.path:
        sys.path.insert(0, r'{path}')

import artistplayblast_
reload(artistplayblast_)
    """.format(path=SourcePath)

        # 
        CurrentShelf = mel.eval('$gShelfTopLevel=$gShelfTopLevel')
        parent   = cmds.tabLayout(CurrentShelf, query=True, selectTab=True)

        cmds.shelfButton(
            command     = artistplayblast_command,
            iol         = "",
            annotation  = "Artist Playblast",
            sourceType  = "python",
            image       = artistplayblast_icon,
            image1      = artistplayblast_icon,
            parent      = parent
        )

    # 
    elif MayaApiVersion() > 20200500:
        print("WARNING: This version is not supported. Your Maya version: " + Ver)
        print("Is it about time to used python 3?")

    # 
    else:
        print("????")




# 
if isMaya:
    onMayaDropped()
    # print("Installing {}".format(tool_name))
# else:
#     print("WARNING: Setup doesn't work. This is not Maya.")