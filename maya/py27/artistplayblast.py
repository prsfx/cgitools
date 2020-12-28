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
        self.artistPlayblast_lbl.setText(str(__tool_name__))

        # set version
        self.artistPlayblast_lbl.setText(str(__version__))


        # menubar start

        # 

        # menubar end


        # icon
        icon = QIcon(Source + "/icons/artistPlayblast/artistPlayblast_icon.png")
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


        # load time range
        self.__loadTimeRange()

        # get artist workstation name
        self.__getUserWorkstation()

        # artist toggle default
        self.artistDefault_chkbx.toggled.connect(self.__artistDefaultToggle)

        # toggle artist name
        self.artistNameEnable_pbttn.clicked.connect(self.__artistNameToggle)

        # get scene file name
        self.__getSceneFile()

        # project toggle default
        self.fileNameDefault_chkbx.toggled.connect(self.__projectDefaultToggle)

        # toggle project name
        self.fileNameEnable_pbttn.clicked.connect(self.__projectNameToggle)

        # get directory folder
        self.__getDirecoryFolder()

        # dir toggle default
        self.directoryDefault_chkbx.toggled.connect(self.__togleDefaultDir)

        # browse set folder
        self.directoryEnableBrowse_pbttn.clicked.connect(self.__browseDirectory)


        # display toggle
        self.currentFrame_pbttn.clicked.connect(self.__showCurrentFrame)
        self.evaluation_pbttn.clicked.connect(self.__showEvaluation)

        self.frameRate_pbttn.clicked.connect(self.__showFrameRate)
        self.sceneTimecode_pbttn.clicked.connect(self.__showSceneTimeCode)

        self.objectDetails_pbttn.clicked.connect(self.__showObjectDetails)
        self.focalLength_pbttn.clicked.connect(self.__showFocalLength)

        self.particleCount_pbttn.clicked.connect(self.__showParticleCount)
        self.polyCount_pbttn.clicked.connect(self.__showPolyCount)

        self.xGen_pbttn.clicked.connect(self.__showXgenInfo)
        self.bifrost_pbttn.clicked.connect(self.__showBifrostParticle)


        # do playblast
        self.playblast_pbttn.clicked.connect(self.__doPlayblast)




    # menubar start

    # 

    # menubar end




    # restore artist playblast
    def __restoreArtistPlayblast(self, *args):
        import artistPlayblast
        reload(artistPlayblast)


    # load camera list
    def __loadCameraList(self, *args):
        print("load camera list...\n")
        cameraList = cmds.ls(type="camera", sn=True)
        camMsg1 = "Camera list: "
        print(camMsg1 + str(cameraList))

        self.cameraList_cmbbx.addItems(cameraList)


    # load viewport
    def __loadViewport(self, *args):
        print("Checking viewport\n")


    # load format and encoding
    def __loadFormatEncoding(self, *args):
        self.formatList_cmbbx.clear()

        crrntCodec = self.format_cmbbx.currentText()

        qtEncoding = (
            "H.264",
            "Cinepak",
            "DV/DVCPRO",
            "DV - PAL",
            "DVCPRO - PAL",
            "H.261",
            "H.263",
            "Photo - JPEG",
            "JPEG 2000",
            "Motion JPEG A",
            "Motion JPEG B",
            "MPEG-4 Video",
            "PNG",
            "None",
            "Animation",
            "Video",
            "Graphics",
            "TGA",
            "TIFF",
            "Component Video",
            "Planar RGB",
            "Sorenson Video",
            "Sorenson Video 3",
            "BMP"
        )

        aviEncoding = (
            "IYUV code",
            "MS-RLE",
            "MS-CRAM",
            "MS-YUV",
            "Toshiba YUV 411",
            "x264vfw",
            "Huffyuv",
            "Lagarith",
            "XVID",
            "none"
        )

        imageEncoding = (
            "global",
            "gif",
            "si",
            "rla",
            "tif",
            "tifu",
            "sgi",
            "als",
            "maya",
            "jpg",
            "eps",
            "cin",
            "yuv",
            "tga",
            "bmp",
            "psd",
            "png",
            "dds",
            "psdLayered"
        )

        if crrntCodec == "qt":
            crrntEncoding = self.formatList_cmbbx.addItems(qtEncoding)

        elif crrntCodec == "avi":
            crrntEncoding = self.formatList_cmbbx.addItems(aviEncoding)

        elif crrntCodec == "image":
            crrntEncoding = self.formatList_cmbbx.addItems(imageEncoding)

        else:
            pass


    # camera active toggle
    def __changeActiveViewport(self, *args):
        print("Toggled active viewport\n")
        crcam = self.cameraList_cmbbx.currentText()
        print(crcam)

        cmds.lookThru(crcam)


    # scale quality 02.5
    def __changeScaleInputOne(self, *args):
        print("Set scale playblast to 0.25\n")

        self.scale_dblspnbx.setValue(0.25)

        self.scale_sldr.setValue(25)


    # scale quality 0.50
    def __changeScaleInputTwo(self, *args):
        print("Set scale playblast to 0.50\n")

        self.scale_dblspnbx.setValue(0.50)

        self.scale_sldr.setValue(50)


    # scale quality 0.75
    def __changeScaleInputThree(self, *args):
        print("Set scale playblast to 0.75\n")

        self.scale_dblspnbx.setValue(0.75)

        self.scale_sldr.setValue(75)


    # scale quality 1.00
    def __changeScaleInputFour(self, *args):
        print("Set scale playblast to 1.00\n")

        self.scale_dblspnbx.setValue(1.00)

        self.scale_sldr.setValue(100)


    # scale to slider
    def __changeTickSlider(self, *args):
        inputVal = self.scale_dblspnbx.value()

        formatVal = inputVal*100

        print(formatVal)

        self.scale_sldr.setValue(formatVal)


    # scale slider
    def __changeScaleInputTick(self, *args):
        nptscl = self.scale_dblspnbx.value()

        tcksldr = float(self.scale_sldr.value())

        msvalue = (tcksldr/100)

        self.scale_dblspnbx.setValue(msvalue)


    # resolution changed input
    def __changeResinput(self, *args):
        rescrinpt = self.resolutionList_cmbbx.currentText()

        if rescrinpt == "HVGA":
            self.widthInput_lndt.setText("480")
            self.heightInput_lndt.setText("320")

        elif rescrinpt == "WVGA":
            self.widthInput_lndt.setText("800")
            self.heightInput_lndt.setText("480")

        elif rescrinpt == "720p":
            self.widthInput_lndt.setText("1280")
            self.heightInput_lndt.setText("720")

        elif rescrinpt == "1080p":
            self.widthInput_lndt.setText("1920")
            self.heightInput_lndt.setText("1080")

        elif rescrinpt == "QHD":
            self.widthInput_lndt.setText("2560")
            self.heightInput_lndt.setText("1440")

        elif rescrinpt == "UHD":
            self.widthInput_lndt.setText("3840")
            self.heightInput_lndt.setText("2160")

        else:
            cmds.warning("No can do that.")


    # load format list
    def __loadFormatList(self, *args):
        crntFormat = self.format_cmbbx.currentText()

        if crntFormat == "qt":
            print("Load *.mov encoding")
            self.__loadFormatEncoding()

        elif crntFormat == "avi":
            print("Load *.avi encoding")
            self.__loadFormatEncoding()

        elif crntFormat == "image":
            print("Load *.image encoding")
            self.__loadFormatEncoding()

        else:
            pass


    # quality slider
    def __qualitySlider(self, *args):
        tcksldr = float(self.quality_sldr.value())

        msvalue = (tcksldr/1)

        self.qualityInput_lndt.setValue(msvalue)


    # quality to tick slider
    def __qualityTickChanged(self, *args):
        inputVal = self.qualityInput_lndt.value()

        '''formatVal = inputVal*100

        print(formatVal)'''

        self.quality_sldr.setValue(inputVal)




    # load time range
    def __loadTimeRange(self, *args):
        timeStart = cmds.playbackOptions(q=True, min=True)

        timeEnd = cmds.playbackOptions(q=True, max=True)

        self.rangeStartInput_lndt.setValue(timeStart)
        self.rangeEndInput_lndt.setValue(timeEnd)


    # get artist workstation name
    def __getUserWorkstation(self, *args):
        print("Looking artist workstation\n")
        self.artistName_lndt.setText(CheckUser)


    # artist toggle default
    def __artistDefaultToggle(self, *args):
        if self.artistDefault_chkbx.isChecked() == True:
            self.__getUserWorkstation()
        else:
            pass


    # toggle artist name
    def __artistNameToggle(self, *args):
        artistName = self.artistName_lndt.text()

        if self.artistNameEnable_pbttn.isChecked() == True:
            cmds.headsUpDisplay("ArtistName", section=6, block=0, blockSize="small", label="Artist:         "+artistName, labelFontSize="small")
        else:
            cmds.headsUpDisplay("ArtistName", rem=True)


    # get scene file
    def __getSceneFile(self, *args):
        print("Looking scene file\n")
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        raw_name, extension = os.path.splitext(filename)

        self.fileNameInput_lndt.setText(raw_name)


    # artist toggle default
    def __projectDefaultToggle(self, *args):
        if self.fileNameDefault_chkbx.isChecked() == True:
            self.__getSceneFile()
        else:
            pass


    # toggle project name
    def __projectNameToggle(self, *args):
        projectName = self.fileNameInput_lndt.text()

        if self.fileNameEnable_pbttn.isChecked() == True:
            cmds.headsUpDisplay("ProjectName", section=8, block=0, blockSize="small", label="Project:         "+projectName, labelFontSize="small")
        else:
            cmds.headsUpDisplay("ProjectName", rem=True)


    # get directory folder
    def __getDirecoryFolder(self, *args):
        print("Load directory folder\n")
        self.directoryInput_lndt.setText(dfprjct+"/movies/")


    # dir toggle default
    def __togleDefaultDir(self, *args):
        projectDir = self.directoryInput_lndt.text()

        if self.directoryDefault_chkbx.isChecked() == True:
            self.directoryInput_lndt.setText(dfprjct+"/movies/")
        else:
            pass


    # browse set folder
    def __browseDirectory(self, *args):
        print("Browse and set directory...\n")
        browseDialog = cmds.fileDialog2(dir=Home, cap="Set Directory...", ds=2, fm=3, hne=True, okc="Set")

        start = str(browseDialog)

        phase1 = start.replace("[u'", "")

        result = phase1.replace("']", "")

        self.directoryInput_lndt.setText(result+"/")




    # display toggle
    def __showCurrentFrame(self, *args):
        cmds.ToggleCurrentFrame()

    def __showEvaluation(self, *args):
        cmds.ToggleEvaluationManagerVisibility()

    def __showFrameRate(self, *args):
        cmds.ToggleFrameRate()

    def __showSceneTimeCode(self, *args):
        cmds.ToggleSceneTimecode()

    def __showObjectDetails(self, *args):
        cmds.ToggleObjectDetails()

    def __showFocalLength(self, *args):
        cmds.ToggleFocalLength()

    def __showParticleCount(self, *args):
        cmds.ToggleParticleCount()

    def __showPolyCount(self, *args):
        cmds.TogglePolyCount()

    def __showXgenInfo(self, *args):
        cmds.ToggleXGenDisplayHUD()

    def __showBifrostParticle(self, *args):
        cmds.DisplayBifrostHUD()




    # do playblast
    def __doPlayblast(self, *args):
        print("Execute Playblast..")
        # cmds.playblast(uts=True) https://help.autodesk.com/cloudhelp/2019/ENU/Maya-Tech-Docs/CommandsPython/playblast.html

        fni = self.fileNameInput_lndt.text()
        dfi = self.directoryInput_lndt.text()
        fnp1 = str(fni)
        dfp1 = str(dfi)
        print("File name:")
        print(fnp1)
        print("Directory:")
        print(dfp1)
        print("")


        ci = self.format_cmbbx.currentText()
        ei = self.formatList_cmbbx.currentText()
        cr = str(ci)
        er = str(ei)
        print("Format:")
        print(cr)
        print("Compression:")
        print(er)
        print("")


        wi = self.widthInput_lndt.text()
        hi = self.heightInput_lndt.text()
        wr = int(wi)
        hr = int(hi)
        print("Width:")
        print(wr)
        print("Height:")
        print(hr)
        print("")


        qi = self.qualityInput_lndt.value()
        si = self.scale_dblspnbx.value()
        qs = int(qi)
        ss = int(si)*100
        print("Quality:")
        print(qs)
        print("Scale:")
        print(ss)
        print("")


        sf = self.rangeStartInput_lndt.value()
        ef = self.rangeEndInput_lndt.value()
        print("Starting frame:")
        print(sf)
        print("End frame:")
        print(ef)
        print("")


        ac = self.cameraList_cmbbx.currentText()
        print("Camera name:")
        print(ac)
        print("")



        if self.format_cmbbx.currentText() == "qt":
            print("*.mov encoding..")
            result = cmds.playblast(useTraxSounds=True, clearCache=True, format="qt", filename=dfp1+fni+".mov", compression=ei, forceOverwrite=True, quality=qs, percent=ss, framePadding=4, startTime=sf, endTime=ef, widthHeight=(wr, hr), viewer=True)
            print(str(result))

        elif self.format_cmbbx.currentText() == "avi":
            print("*.avi encoding..")
            result = cmds.playblast(useTraxSounds=True, clearCache=True, format="avi", filename=dfp1+fni+".avi", compression=ei, forceOverwrite=True, quality=qs, percent=ss, framePadding=4, startTime=sf, endTime=ef, widthHeight=(wr, hr), viewer=True)
            print(str(result))

        elif self.format_cmbbx.currentText() == "image":
            print("image encoding..")
            result = cmds.playblast(useTraxSounds=True, clearCache=True, format="image", indexFromZero=True, filename=dfp1+fni+"."+ei, compression=ei, forceOverwrite=True, quality=qs, percent=ss, framePadding=4, startTime=sf, endTime=ef, widthHeight=(wr, hr), viewer=True)
            print(str(result))

        else:
            pass




    def closeEvent(self, *args):
        self.parent().deleteLater()
        self.parent().close()




# artist playblast mixin class
class artistPlayblastMixinWindowDock(MayaQWidgetDockableMixin, artistplayblast.artistPlayblastUI):

    artistplayblast_name = artistplayblast_mixin_windowname

    def __init__(self, parent=None):
        self.deleteInstances()

        super(artistPlayblastMixinWindowDock, self).__init__(parent)

        MayaMainWindow()

        self.setWindowTitle(artistplayblast_mixin_windowname)

        self.setWindowFlags(QtCore.Qt.Window)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


    def dockCloseEventTriggered(self, *args):
        self.deleteInstances()


    def deleteInstances(self, *args):
        for obj in MayaMainWindow().children():
            if str(type(obj)) == artistPlayblastMixinWindowDock:
                if obj.widget().objectName() == self.__class__.artistplayblast_name:
                    print('Deleting instance {0}'.format(obj))
                    MayaMainWindow().removeDockWidget(obj)
                    obj.setParent(None)
                    obj.deleteLater()


    def deleteControl(self, control):

        if cmds.workspaceControl(control, q=True, exists=True):
            cmds.workspaceControl(control, e=True, close=True)
            cmds.deleteUI(control, control=True)


    def run(self):

        self.setObjectName(artistplayblast_mixin_windowname)

        workspaceControlName = self.objectName() + "WorkspaceControl"
        self.deleteControl(workspaceControlName)

        self.show(dockable=True, area="left", floating=True)
        cmds.workspaceControl(workspaceControlName, e=True, ttc=["Outliner", 2], wp="preferred", mw=302)
        self.raise_()

        self.setDockableParameters(width=302)




# 
def launchUI():

    artistplayblast_mixinwindow = artistPlayblastMixinWindowDock()
    artistplayblast_mixinwindow.run()

    return artistplayblast_mixinwindow


# 
def main(*args, **kwargs):
    if artistplayblast.isMaya():
        launch_tool = launchUI()
        cmds.inViewMessage( amg='prsfx: <hl>" check your codec properly.. Then you are good to go..."</hl>.', pos='topRight', fade=True )
    else:
        launch_tool = "Emm, something not right with the API and version"
        print(launch_tool)
        cmds.inViewMessage( amg='warning: <hl>" {}"</hl>.'.format(launch_tool), pos='topRight', fade=True )

    return launch_tool




# 
if __name__ == "__main__":
    reload(artistplayblast)
    with artistplayblast.app():
        artistplayblast.main()