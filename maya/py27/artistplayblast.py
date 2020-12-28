# -*- coding: utf-8 -*-

MAJOR = 0
MINOR = 1
PATCH = 2


# 
__tool_name__ = "Artist Playblast"
__version__ = "v{}.{}.{}".format(MAJOR, MINOR, PATCH)

__release__ = __tool_name__ + __version__


# 
import os
import sys
import platform
import getpass


import artistplayblast


from os.path import expanduser

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.LoDb import *
from config.LoDb import defaultBind
from config.LoDb import loadUiType
from config.LoDb import wrapinstance

from cStringIO import StringIO

from maya import mel as mel
from maya import cmds as cmds
from maya import OpenMayaUI as omui

from maya.api import OpenMaya

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin




# 
Source      = os.path.dirname(__file__)
SourcePath  = os.path.normpath(os.path.join(Source))

Ver         = int(cmds.about(api=True))
CheckOS     = platform.system()
CheckUser   = getpass.getuser()
CheckPyVer  = sys.version
Home        = expanduser("~")

slctn       = cmds.ls(sl=True)

dfprjct     = cmds.workspace(q=True, o=True)




def MayaMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapinstance(long(main_window_ptr), QtWidgets.QWidget)

def isMaya():
    try:
        import maya.cmds as cmds
        cmds.about(batch=True)
        return True
    except ImportError:
        return False




# 
artistplayblast_mixin_windowname = __release__
artistplayblast_mixin_dockname = __release__


# 
artistplayblast_form, artistplayblast_base = loadUiType(SourcePath + "/layouts/artistplayblast_interface.ui")




# artist playblast main class
class artistPlayblastUI(artistplayblast_form, artistplayblast_base):
    def __init__(self, parent=None):
        super(artistPlayblastUI, self).__init__(parent)

        # start to setup
        self.setupUi(self)

        # tool name
        self.artistPlayblast_lbl.setText(__tool_name__)

        # set version
        self.artistPlayblast_lbl.setText(__version__)


        # menubar start

        # 

        # menubar end


        # icon
        icon = QIcon(os.path.join(os.getcwd(), "/icons/artistplayblast-icon.png"))
        self.artistPlayblastIcon_pbttn.setIcon(icon)


        # restore artist playblast
        self.artistPlayblastIcon_pbttn.clicked.connect(self.__restoreArtistPlayblast)

        # load camera list
        self.__loadCameraList()

        # load viewport
        self.__loadViewport()

        # load format and encoding
        self.__loadFormatEncoding()

        # camera active toggle
        self.cameraList_cmbbx.currentTextChanged.connect(self.__changeActiveViewport)

        # scale quality 0.25
        self.quarterScale_pbttn.clicked.connect(self.__changeScaleInputOne)

        # scale quality 0.50
        self.halfScale_pbttn.clicked.connect(self.__changeScaleInputTwo)

        # scale quality 0.75
        self.halfQuarterScale_pbttn.clicked.connect(self.__changeScaleInputThree)

        # scale quality 1.00
        self.fullScale_pbttn.clicked.connect(self.__changeScaleInputFour)

        # scale to slider
        self.scale_dblspnbx.valueChanged.connect(self.__changeTickSlider)

        # scale slider
        self.scale_sldr.valueChanged.connect(self.__changeScaleInputTick)

        # wh input
        self.widthInput_lndt.setText("480")
        self.heightInput_lndt.setText("320")

        # resolution changed input
        self.resolutionList_cmbbx.currentTextChanged.connect(self.__changeResinput)

        # load format list
        self.format_cmbbx.currentTextChanged.connect(self.__loadFormatList)

        # quality slider
        self.quality_sldr.valueChanged.connect(self.__qualitySlider)

        # quality to tick slider
        self.qualityInput_lndt.valueChanged.connect(self.__qualityTickChanged)