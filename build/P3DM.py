# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mesh.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
# 

from os.path import isfile
from os import getcwd, environ, remove, path
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import axes3d, Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import PTN_LIBRARY.ptn_library as PTN 
import numpy as np 
from time import time

from math import sqrt, radians 
from operator import mul as OP_mul 
import win32gui
import SMART_Input_UI as SMART 
import RegDB as regDB
import warnings 

try: 
    import paramiko as FTP 
except: 
    print ("No paramiko module.. ")

class StdoutRedirect(QtCore.QObject):
    printOccur = QtCore.pyqtSignal(str, str, name="print")
 
    def __init__(self, *param):
        QtCore.QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write
 
    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr
 
    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg : self.write(msg, color="red")
 
    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        try: 
            remove("currentSmartInput.tmp")
        except: 
            pass

        self.mainWindowName = "P3DM - pattern mesh expansion"
        warnings.filterwarnings('ignore')

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("tire.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        Width_command=300 
        btn_ht = 25 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_auto = QtWidgets.QPushButton(self.centralwidget)
        self.btn_auto.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_auto.setMaximumSize(QtCore.QSize(300, 30))
        self.btn_auto.setObjectName("btn_auto")
        self.verticalLayout.addWidget(self.btn_auto)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sectorno = QtWidgets.QLabel(self.centralwidget)
        self.sectorno.setMaximumSize(QtCore.QSize(50, 25))
        self.sectorno.setObjectName("sectorno")
        self.horizontalLayout_2.addWidget(self.sectorno)
        self.input_layout_sector = QtWidgets.QLineEdit(self.centralwidget)
        self.input_layout_sector.setMaximumSize(QtCore.QSize(50, 25))
        self.input_layout_sector.setAlignment(QtCore.Qt.AlignCenter)
        self.input_layout_sector.setObjectName("input_layout_sector")
        self.horizontalLayout_2.addWidget(self.input_layout_sector)
        self.pitchno = QtWidgets.QLabel(self.centralwidget)
        self.pitchno.setMaximumSize(QtCore.QSize(50, 25))
        self.pitchno.setObjectName("pitchno")
        self.horizontalLayout_2.addWidget(self.pitchno)
        self.input_pitch_no = QtWidgets.QLineEdit(self.centralwidget)
        self.input_pitch_no.setMaximumSize(QtCore.QSize(50, 25))
        self.input_pitch_no.setAlignment(QtCore.Qt.AlignCenter)
        self.input_pitch_no.setObjectName("input_pitch_no")
        self.horizontalLayout_2.addWidget(self.input_pitch_no)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_layoutmesh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_layoutmesh.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_layoutmesh.setMaximumSize(QtCore.QSize(145, 30))
        self.btn_layoutmesh.setObjectName("btn_layoutmesh")
        self.horizontalLayout_3.addWidget(self.btn_layoutmesh)
        self.btn_patternmesh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_patternmesh.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_patternmesh.setMaximumSize(QtCore.QSize(145, 30))
        self.btn_patternmesh.setObjectName("btn_patternmesh")
        self.horizontalLayout_3.addWidget(self.btn_patternmesh)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.layoutfile = QtWidgets.QLabel(self.centralwidget)
        self.layoutfile.setMinimumSize(QtCore.QSize(0, 15))
        self.layoutfile.setMaximumSize(QtCore.QSize(250, 15))
        self.layoutfile.setObjectName("layoutfile")
        self.verticalLayout.addWidget(self.layoutfile)
        self.patternfile = QtWidgets.QLabel(self.centralwidget)
        self.patternfile.setMinimumSize(QtCore.QSize(0, 15))
        self.patternfile.setMaximumSize(QtCore.QSize(250, 15))
        self.patternfile.setObjectName("patternfile")
        self.verticalLayout.addWidget(self.patternfile)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.ABAQUS = QtWidgets.QCheckBox(self.centralwidget)
        self.ABAQUS.setObjectName("ABAQUS")
        self.horizontalLayout_6.addWidget(self.ABAQUS)
        self.check_T3DM = QtWidgets.QCheckBox(self.centralwidget)
        self.check_T3DM.setObjectName("check_T3DM")
        self.horizontalLayout_6.addWidget(self.check_T3DM)
        self.check_FricView = QtWidgets.QCheckBox(self.centralwidget)
        self.check_FricView.setObjectName("check_FricView")
        self.horizontalLayout_6.addWidget(self.check_FricView)
        self.check_SubTread = QtWidgets.QCheckBox(self.centralwidget)
        self.check_SubTread.setObjectName("check_SubTread")
        self.horizontalLayout_6.addWidget(self.check_SubTread)
        self.check_Direction = QtWidgets.QCheckBox(self.centralwidget)
        self.check_Direction.setObjectName("check_Direction")
        self.horizontalLayout_6.addWidget(self.check_Direction)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_removetread = QtWidgets.QPushButton(self.centralwidget)
        self.btn_removetread.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_removetread.setMaximumSize(QtCore.QSize(95, 30))
        self.btn_removetread.setObjectName("btn_removetread")
        self.horizontalLayout_4.addWidget(self.btn_removetread)
        self.btn_expansion = QtWidgets.QPushButton(self.centralwidget)
        self.btn_expansion.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_expansion.setMaximumSize(QtCore.QSize(95, 30))
        self.btn_expansion.setObjectName("btn_expansion")
        self.horizontalLayout_4.addWidget(self.btn_expansion)
        self.btn_generation = QtWidgets.QPushButton(self.centralwidget)
        self.btn_generation.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_generation.setMaximumSize(QtCore.QSize(95, 30))
        self.btn_generation.setObjectName("btn_generation")
        self.horizontalLayout_4.addWidget(self.btn_generation)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupbox_layout = QtWidgets.QGroupBox(self.centralwidget)
        self.groupbox_layout.setMinimumSize(QtCore.QSize(300, 45))
        self.groupbox_layout.setMaximumSize(QtCore.QSize(300, 120))
        self.groupbox_layout.setObjectName("Horizontal_radio_layout")
        self.radio_currentlayout = QtWidgets.QRadioButton(self.groupbox_layout)
        self.radio_currentlayout.setGeometry(QtCore.QRect(10, 20, 90, 16))
        self.radio_currentlayout.setObjectName("radio_currentlayout")
        self.radio_layout = QtWidgets.QRadioButton(self.groupbox_layout)
        self.radio_layout.setGeometry(QtCore.QRect(90, 20, 90, 16))
        self.radio_layout.setObjectName("radio_layout")
        self.radio_untreaded = QtWidgets.QRadioButton(self.groupbox_layout)
        self.radio_untreaded.setGeometry(QtCore.QRect(160, 20, 111, 16))
        self.radio_untreaded.setObjectName("radio_untreaded")
        self.checkBox_No = QtWidgets.QCheckBox(self.groupbox_layout)
        self.checkBox_No.setGeometry(QtCore.QRect(90, 0, 81, 16))
        self.checkBox_No.setObjectName("checkBox_No")
        self.horizontalLayout_8.addWidget(self.groupbox_layout)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.groupbox_patternstatus = QtWidgets.QGroupBox(self.centralwidget)
        self.groupbox_patternstatus.setMinimumSize(QtCore.QSize(300, 65))
        self.groupbox_patternstatus.setMaximumSize(QtCore.QSize(300, 65))
        self.groupbox_patternstatus.setObjectName("Horizontal_radio_stage")
        self.radio_model = QtWidgets.QRadioButton(self.groupbox_patternstatus)
        self.radio_model.setGeometry(QtCore.QRect(10, 20, 90, 16))
        self.radio_model.setObjectName("radio_model")
        self.radio_scaled = QtWidgets.QRadioButton(self.groupbox_patternstatus)
        self.radio_scaled.setGeometry(QtCore.QRect(90, 20, 90, 16))
        self.radio_scaled.setObjectName("radio_expanded")
        self.radio_gauged = QtWidgets.QRadioButton(self.groupbox_patternstatus)
        self.radio_gauged.setGeometry(QtCore.QRect(190, 20, 111, 16))
        self.radio_gauged.setObjectName("radio_gauged")
        self.radio_bended = QtWidgets.QRadioButton(self.groupbox_patternstatus)
        self.radio_bended.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.radio_bended.setObjectName("radio_bended")
        self.radio_expanded = QtWidgets.QRadioButton(self.groupbox_patternstatus)
        self.radio_expanded.setGeometry(QtCore.QRect(90, 40, 111, 20))
        self.radio_expanded.setObjectName("radio_btmnode")
        self.horizontalLayout_23.addWidget(self.groupbox_patternstatus)
        self.verticalLayout.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.Horizontal_radio = QtWidgets.QGroupBox(self.centralwidget)
        self.Horizontal_radio.setMinimumSize(QtCore.QSize(300, 65))
        self.Horizontal_radio.setMaximumSize(QtCore.QSize(300, 65))
        self.Horizontal_radio.setObjectName("Horizontal_radio")
        self.radioDefault = QtWidgets.QRadioButton(self.Horizontal_radio)
        self.radioDefault.setGeometry(QtCore.QRect(10, 20, 90, 16))
        self.radioDefault.setObjectName("radioDefault")
        self.radioTop = QtWidgets.QRadioButton(self.Horizontal_radio)
        self.radioTop.setGeometry(QtCore.QRect(90, 20, 90, 16))
        self.radioTop.setObjectName("radioTop")
        self.radioBottom = QtWidgets.QRadioButton(self.Horizontal_radio)
        self.radioBottom.setGeometry(QtCore.QRect(160, 20, 111, 16))
        self.radioBottom.setObjectName("radioBottom")
        self.checkBox_SurfNo = QtWidgets.QCheckBox(self.Horizontal_radio)
        self.checkBox_SurfNo.setGeometry(QtCore.QRect(140, 0, 81, 16))
        self.checkBox_SurfNo.setObjectName("checkBox_SurfNo")
        self.radioPitch = QtWidgets.QRadioButton(self.Horizontal_radio)
        self.radioPitch.setGeometry(QtCore.QRect(10, 40, 111, 16))
        self.radioPitch.setObjectName("radioPitch")
        self.radioSide = QtWidgets.QRadioButton(self.Horizontal_radio)
        self.radioSide.setGeometry(QtCore.QRect(160, 40, 111, 16))
        self.radioSide.setObjectName("radioSide")
        self.horizontalLayout_24.addWidget(self.Horizontal_radio)
        self.verticalLayout.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.groupBox_OverlaySurf = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_OverlaySurf.setMinimumSize(QtCore.QSize(300, 65))
        self.groupBox_OverlaySurf.setMaximumSize(QtCore.QSize(300, 65))
        self.groupBox_OverlaySurf.setObjectName("groupBox_6")
        self.radio_Maingrv = QtWidgets.QRadioButton(self.groupBox_OverlaySurf)
        self.radio_Maingrv.setGeometry(QtCore.QRect(10, 20, 90, 16))
        self.radio_Maingrv.setObjectName("radioMaingrvBtm")
        
        self.checkBox_OverlaySurfNo = QtWidgets.QCheckBox(self.groupBox_OverlaySurf)
        self.checkBox_OverlaySurfNo.setGeometry(QtCore.QRect(120, 0, 81, 16))
        self.checkBox_OverlaySurfNo.setObjectName("checkBox_OverlaySurfNo")

        self.radio_Subgrv = QtWidgets.QRadioButton(self.groupBox_OverlaySurf)
        self.radio_Subgrv.setGeometry(QtCore.QRect(160, 20, 111, 16))
        self.radio_Subgrv.setObjectName("radioSubgrvBtm")
        self.radio_Kerf = QtWidgets.QRadioButton(self.groupBox_OverlaySurf)
        self.radio_Kerf.setGeometry(QtCore.QRect(10, 40, 71, 20))
        self.radio_Kerf.setObjectName("radioSubGrv")
        self.radio_AllSide = QtWidgets.QRadioButton(self.groupBox_OverlaySurf)
        self.radio_AllSide.setGeometry(QtCore.QRect(160, 40, 111, 20))
        self.radio_AllSide.setObjectName("radioMainGrv")
        self.horizontalLayout_25.addWidget(self.groupBox_OverlaySurf)
        self.verticalLayout.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.SearchElement = QtWidgets.QLabel(self.centralwidget)
        self.SearchElement.setMinimumSize(QtCore.QSize(0, 25))
        self.SearchElement.setMaximumSize(QtCore.QSize(90, 25))
        self.SearchElement.setObjectName("SearchElement")
        self.horizontalLayout_7.addWidget(self.SearchElement)
        self.searchno = QtWidgets.QLineEdit(self.centralwidget)
        self.searchno.setMinimumSize(QtCore.QSize(0, 25))
        self.searchno.setMaximumSize(QtCore.QSize(150, 25))
        self.searchno.setAlignment(QtCore.Qt.AlignCenter)
        self.searchno.setObjectName("searchno")
        self.horizontalLayout_7.addWidget(self.searchno)
        self.btn_showsolid = QtWidgets.QPushButton(self.centralwidget)
        self.btn_showsolid.setMinimumSize(QtCore.QSize(0, 25))
        self.btn_showsolid.setMaximumSize(QtCore.QSize(45, 25))
        self.btn_showsolid.setObjectName("btn_showsolid")
        self.horizontalLayout_7.addWidget(self.btn_showsolid)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.btn_PtnNodeCheck = QtWidgets.QPushButton(self.centralwidget)
        self.btn_PtnNodeCheck.setMinimumSize(QtCore.QSize(0, 25))
        self.btn_PtnNodeCheck.setMaximumSize(QtCore.QSize(300, 25))
        self.btn_PtnNodeCheck.setObjectName("btn_PtnNodeCheck")
        self.verticalLayout.addWidget(self.btn_PtnNodeCheck)
        self.btn_initialization = QtWidgets.QPushButton(self.centralwidget)
        self.btn_initialization.setMinimumSize(QtCore.QSize(0, 25))
        self.btn_initialization.setMaximumSize(QtCore.QSize(300, 25))
        self.btn_initialization.setObjectName("btn_initialization")
        self.verticalLayout.addWidget(self.btn_initialization)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setMinimumSize(QtCore.QSize(250, 120))
        self.textBrowser.setMaximumSize(QtCore.QSize(300, 16777215))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setMaximumSize(QtCore.QSize(50, 15))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_12.addWidget(self.checkBox)
        self.line_PCI_Press = QtWidgets.QLineEdit(self.centralwidget)
        self.line_PCI_Press.setMaximumSize(QtCore.QSize(30, 20))
        self.line_PCI_Press.setAlignment(QtCore.Qt.AlignCenter)
        self.line_PCI_Press.setObjectName("line_PCI_Press")
        self.horizontalLayout_12.addWidget(self.line_PCI_Press)
        
        self.checkBox_overType = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_overType.setMaximumSize(QtCore.QSize(180, 20))
        self.checkBox_overType.setObjectName("checkBox_overType")
        self.horizontalLayout_12.addWidget(self.checkBox_overType)

        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_bt1 = QtWidgets.QLabel(self.centralwidget)
        self.label_bt1.setMaximumSize(QtCore.QSize(60, 15))
        self.label_bt1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bt1.setObjectName("label_bt1")
        self.horizontalLayout_11.addWidget(self.label_bt1)
        self.lineEdit_bt1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_bt1.setMaximumSize(QtCore.QSize(30, 20))
        self.lineEdit_bt1.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_bt1.setObjectName("lineEdit_bt1")
        self.horizontalLayout_11.addWidget(self.lineEdit_bt1)
        self.label_bt2 = QtWidgets.QLabel(self.centralwidget)
        self.label_bt2.setMaximumSize(QtCore.QSize(25, 15))
        self.label_bt2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bt2.setObjectName("label_bt2")
        self.horizontalLayout_11.addWidget(self.label_bt2)
        self.lineEdit_bt2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_bt2.setMaximumSize(QtCore.QSize(30, 20))
        self.lineEdit_bt2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_bt2.setObjectName("lineEdit_bt2")
        self.horizontalLayout_11.addWidget(self.lineEdit_bt2)
        self.label_bt3 = QtWidgets.QLabel(self.centralwidget)
        self.label_bt3.setMaximumSize(QtCore.QSize(25, 15))
        self.label_bt3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bt3.setObjectName("label_bt3")
        self.horizontalLayout_11.addWidget(self.label_bt3)
        self.lineEdit_bt3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_bt3.setMaximumSize(QtCore.QSize(30, 20))
        self.lineEdit_bt3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_bt3.setObjectName("lineEdit_bt3")
        self.horizontalLayout_11.addWidget(self.lineEdit_bt3)
        self.label_bt4 = QtWidgets.QLabel(self.centralwidget)
        self.label_bt4.setMaximumSize(QtCore.QSize(25, 15))
        self.label_bt4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bt4.setObjectName("label_bt4")
        self.horizontalLayout_11.addWidget(self.label_bt4)
        self.lineEdit_bt4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_bt4.setMaximumSize(QtCore.QSize(30, 20))
        self.lineEdit_bt4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_bt4.setObjectName("lineEdit_bt4")
        self.horizontalLayout_11.addWidget(self.lineEdit_bt4)
        self.verticalLayout.addLayout(self.horizontalLayout_11)


        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_BSD = QtWidgets.QLabel(self.centralwidget)
        self.label_BSD.setMaximumSize(QtCore.QSize(30, 15))
        self.label_BSD.setAlignment(QtCore.Qt.AlignCenter)
        self.label_BSD.setObjectName("label_BSD")
        self.horizontalLayout_13.addWidget(self.label_BSD)
        self.lineEdit_BSD = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_BSD.setMaximumSize(QtCore.QSize(35, 20))
        self.lineEdit_BSD.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_BSD.setObjectName("lineEdit_BSD")
        self.horizontalLayout_13.addWidget(self.lineEdit_BSD)
        self.label_BDWidth = QtWidgets.QLabel(self.centralwidget)
        self.label_BDWidth.setMaximumSize(QtCore.QSize(60, 15))
        self.label_BDWidth.setAlignment(QtCore.Qt.AlignCenter)
        self.label_BDWidth.setObjectName("label_BDWidth")
        self.horizontalLayout_13.addWidget(self.label_BDWidth)
        self.lineEdit_BDWidth = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_BDWidth.setMaximumSize(QtCore.QSize(35, 20))
        self.lineEdit_BDWidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_BDWidth.setObjectName("lineEdit_BDWidth")
        self.horizontalLayout_13.addWidget(self.lineEdit_BDWidth)
        self.label_DesignRW = QtWidgets.QLabel(self.centralwidget)
        self.label_DesignRW.setMaximumSize(QtCore.QSize(60, 15))
        self.label_DesignRW.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DesignRW.setObjectName("label_DesignRW")
        self.horizontalLayout_13.addWidget(self.label_DesignRW)
        self.lineEdit_DesignRW = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_DesignRW.setMaximumSize(QtCore.QSize(40, 20))
        self.lineEdit_DesignRW.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_DesignRW.setObjectName("lineEdit_DesignRW")
        self.horizontalLayout_13.addWidget(self.lineEdit_DesignRW)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        

        # self.message = QtWidgets.QLabel(self.centralwidget)
        # self.message.setMaximumSize(QtCore.QSize(250, 20))
        # self.message.setSizeIncrement(QtCore.QSize(0, 20))
        # self.message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        # self.message.setObjectName("message")
        # self.verticalLayout.addWidget(# self.message)

        self.lineEdit_materialDir = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_materialDir.setMaximumSize(QtCore.QSize(300, 25))
        self.lineEdit_materialDir.setObjectName("lineEdit_materialDir")
        self.verticalLayout.addWidget(self.lineEdit_materialDir)

        
        
        self.btn_material = QtWidgets.QPushButton(self.centralwidget)
        self.btn_material.setMinimumSize(QtCore.QSize(0, 25))
        self.btn_material.setMaximumSize(QtCore.QSize(300, 25))
        self.btn_material.setObjectName("btn_exit")
        self.verticalLayout.addWidget(self.btn_material)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # self.imagebox = QtWidgets.QLabel(self.centralwidget)
        # self.imagebox.setText("")
        # self.imagebox.setObjectName("imagebox")
        # self.verticalLayout_2.addWidget(self.imagebox)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        ############################################################
        ## MENU BAR 
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1523, 31))
        self.menubar.setObjectName("menubar")
        self.menuFILE = QtWidgets.QMenu(self.menubar)
        self.menuFILE.setObjectName("menuFILE")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSMART = QtWidgets.QAction(MainWindow)
        self.actionSMART.setObjectName("actionSMART")

        self.actionMaterial_DB = QtWidgets.QAction(MainWindow)
        self.actionMaterial_DB.setObjectName("actionMaterial_DB")
        self.actionRotatePattern = QtWidgets.QAction(MainWindow)
        self.actionRotatePattern.setObjectName("actionRotatePattern")
        
        self.menuFILE.addAction(self.actionSMART)
        self.menuFILE.addAction(self.actionRotatePattern)
        self.menuFILE.addAction(self.actionMaterial_DB)
        
        self.menubar.addAction(self.menuFILE.menuAction())

        self.menuFILE.setTitle("INP")
        self.actionSMART.setText("SMART")
        self.actionRotatePattern.setText("Generate Rotated ptn")
        self.actionMaterial_DB.setText("Register DB")
        self.actionSMART.triggered.connect(self.openInputWindow)
        self.actionRotatePattern.triggered.connect(self.Generate_Rotated_PTN)
        self.actionMaterial_DB.triggered.connect(self.registerMaterialDB)
        ############################################################


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.btn_auto, self.input_layout_sector)
        MainWindow.setTabOrder(self.input_layout_sector, self.input_pitch_no)
        MainWindow.setTabOrder(self.input_pitch_no, self.btn_layoutmesh)
        MainWindow.setTabOrder(self.btn_layoutmesh, self.btn_patternmesh)
        MainWindow.setTabOrder(self.btn_patternmesh, self.ABAQUS)
        MainWindow.setTabOrder(self.ABAQUS, self.check_T3DM)
        MainWindow.setTabOrder(self.check_T3DM, self.check_FricView)
        MainWindow.setTabOrder(self.check_FricView, self.check_SubTread)
        MainWindow.setTabOrder(self.check_SubTread, self.check_Direction)
        MainWindow.setTabOrder(self.check_Direction, self.btn_removetread)
        MainWindow.setTabOrder(self.btn_removetread, self.btn_expansion)
        MainWindow.setTabOrder(self.btn_expansion, self.btn_generation)
        MainWindow.setTabOrder(self.btn_generation, self.checkBox_No)
        MainWindow.setTabOrder(self.checkBox_No, self.radio_currentlayout)
        MainWindow.setTabOrder(self.radio_currentlayout, self.radio_layout)
        MainWindow.setTabOrder(self.radio_layout, self.radio_untreaded)
        MainWindow.setTabOrder(self.radio_untreaded, self.radio_model)
        MainWindow.setTabOrder(self.radio_model, self.radio_scaled)
        MainWindow.setTabOrder(self.radio_scaled, self.radio_gauged)
        MainWindow.setTabOrder(self.radio_gauged, self.radio_bended)
        MainWindow.setTabOrder(self.radio_bended, self.radio_expanded)
        MainWindow.setTabOrder(self.radio_expanded, self.checkBox_SurfNo)
        MainWindow.setTabOrder(self.checkBox_SurfNo, self.radioDefault)
        MainWindow.setTabOrder(self.radioDefault, self.radioTop)
        MainWindow.setTabOrder(self.radioTop, self.radioBottom)
        MainWindow.setTabOrder(self.radioBottom, self.radioPitch)
        MainWindow.setTabOrder(self.radioPitch, self.radioSide)
        MainWindow.setTabOrder(self.radioSide, self.radio_Maingrv)
        MainWindow.setTabOrder(self.radio_Maingrv, self.radio_Subgrv)
        MainWindow.setTabOrder(self.radio_Subgrv, self.radio_Kerf)
        MainWindow.setTabOrder(self.radio_Kerf, self.radio_AllSide)
        MainWindow.setTabOrder(self.radio_AllSide, self.searchno)
        MainWindow.setTabOrder(self.searchno, self.btn_showsolid)
        MainWindow.setTabOrder(self.btn_showsolid, self.btn_PtnNodeCheck)
        MainWindow.setTabOrder(self.btn_PtnNodeCheck, self.btn_initialization)
        MainWindow.setTabOrder(self.btn_initialization, self.textBrowser)
        MainWindow.setTabOrder(self.textBrowser, self.btn_material)

        self.dfile = "pdir.dir"
        cwd =getcwd()
        if isfile(self.dfile) == False: 
            df = cwd + '/' +self.dfile
            self.cwd=writeworkingdirectory(df, dfile=self.dfile)
        else: 
            f = open(self.dfile, 'r')
            line =f.readlines()
            f.close()
            self.cwd =line[0]

        self.Pattern_start_number = 10**7 
        self.user_number_pitch = 0 
        self.default_pitch = 0
        self.user_sector = 0 
        self.patternmesh = ""
        self.layoutmesh  = ""
        self.treadremoved = 0 
        self.patternexpanded = 0 
        self.openlayout = 0
        self.openpattern = 0 
        self.filesaved = 0 
        self.renewptn = 0 
        self.renewlayout = 0 
        self.PI = 3.14159265358979323846
        self.errorcode = 0 
        self.LayoutNo = 0 
        self.savedirectory = ''
        self.flattened_Tread_bottom_sorted=[]
        self.shoulderGa = 0
        self.ptn_elset=[]
        self.poffset=10000
        self.ptn_btm_node_section = []

        self.reversed_pattern =  -1 
        self.Check_ShoulderGaugeCheck = 1

        self.readlayout = 0;         self.readpattern = 0 
        # self.SubTread = 1 

        self.btn_auto.clicked.connect(self.autogeneration)
        self.btn_layoutmesh.clicked.connect(self.open_layout)
        self.btn_patternmesh.clicked.connect(self.open_pattern)
        self.btn_removetread.clicked.connect(self.removal_tread)
        self.btn_expansion.clicked.connect(self.expansion_ptn)
        self.btn_generation.clicked.connect(self.generation_mesh)
        self.btn_initialization.clicked.connect(self.Initilize)
        self.btn_material.clicked.connect(self.Update_ISLM_Material)
        self.btn_PtnNodeCheck.clicked.connect(self.ptn_checking)
        self.btn_showsolid.clicked.connect(self.showsolid)
        self.searchno.returnPressed.connect(self.showsolid)



        ## radio button 
        self.radio_currentlayout.clicked.connect(self.showcurrentlayout)
        self.radio_layout.clicked.connect(self.showlayout)
        self.radio_untreaded.clicked.connect(self.showuntreaded)
        self.radioTop.clicked.connect(self.showTopSurface)
        self.radioBottom.clicked.connect(self.showBottomSurface)
        self.radio_Maingrv.clicked.connect(self.showMainGrvBtm)
        self.radio_Subgrv.clicked.connect(self.showSubGrvBtm)
        self.radio_AllSide.clicked.connect(self.showMainGroove)
        self.radio_Kerf.clicked.connect(self.showSubGroove)
        self.radioDefault.clicked.connect(self.showDefault)
        self.radioPitch.clicked.connect(self.showPitch)
        self.radioSide.clicked.connect(self.showSide)

        

        self.sfile = "status.sta"
        if isfile(self.sfile) == False: 
            writestatus( dfile=self.sfile, new=1)
        else: 
            with open(self.sfile) as IN:
                line = IN.readlines()
            state = list(line[0].split(","))
            FricView = int(state[0])
            t3d = int(state[1])
            sut  = int(state[2])
            rev  = int(state[3])
            if len(state) >4 : 
                abq  = int(state[4])
            else: 
                abq = 0 

            if FricView == 1:  self.check_FricView.setChecked(True)
            if t3d == 1:   self.check_T3DM.setChecked(True)
            if sut == 1:   self.check_SubTread.setChecked(True) 
            if abq == 1:   self.ABAQUS.setChecked(True)

        self.checkBox_No.stateChanged.connect(self.showLayoutNo)
        self.check_T3DM.stateChanged.connect(self.T3DM_Checking)
        self.check_SubTread.stateChanged.connect(self.SUT_Checking)
        self.check_FricView.stateChanged.connect(self.FricView_Checking)
        # self.check_Direction.stateChanged.connect(self.PTN_Direction_Change)
        self.ABAQUS.stateChanged.connect(self.ABAQUS_Checking)
       


        self.radio_model.clicked.connect(self.showmodel)
        self.radio_scaled.clicked.connect(self.showexpanded)
        self.radio_gauged.clicked.connect(self.showgauged)
        self.radio_bended.clicked.connect(self.showbended)
        self.radio_expanded.clicked.connect(self.showbottomed)

        self.figure = myCanvas()
        self.canvas = self.figure.canvas
        self.toolbar = self.figure.toolbar 

        self.verticalLayout_2.addWidget(self.toolbar)
        self.verticalLayout_2.addWidget(self.canvas)

        self.btn_expansion.setDisabled(True)
        self.btn_removetread.setDisabled(True)
        self.btn_generation.setDisabled(True)
        self.searchsolid = []

        # self._stdout = StdoutRedirect()
        # self._stdout.start()
        # self._stdout.printOccur.connect(lambda x : self._append_text(x))

        self.P3DMLayout = 0 
        self.P3DMPattern = 0  
        self.ShowingImage = 'none'
        
        self.fullmeshSave=""

        self.localCordDB = 'ISLM_CordDB.txt'
        self.fileListFile = 'ISLM_materialList.txt'
        self.ISLM_cordDBFile="ISLM_CordDBName.dat"

        self.materialDBfilename = "materialdb.dat"

        try: 
            with open(self.materialDBfilename) as DB: 
                lines = DB.readlines()
        except:
            f = open(self.materialDBfilename, 'w')
            ip = '10.82.66.65'
            f.write(ip+"\n")
            id = 'h20200155'
            f.write(id+"\n")
            pw = 'h20200155'
            f.write(pw+"\n")
            f.close()
        
    def registerMaterialDB(self): 
        DialogReg = QtWidgets.QDialog()
        dlgReg = regDB.Ui_Dialog()
        dlgReg.setupUi(DialogReg)
        DialogReg.exec_()

    def openInputWindow(self):
        if self.fullmeshSave != "": 
            # try:
                try: 
                    PCIPress = float(self.line_PCI_Press.text())
                    PCIPress = PCIPress
                except:
                    print ("# Check PCI Press")
                    PCIPress = 0.0
                    return 
                try: 
                    bsd = float(self.lineEdit_BSD.text())
                    bsd = bsd
                except:
                    print ("# Check BSD")
                    bsd = 0.0
                    return 
                try: 
                    bdw = float(self.lineEdit_BDWidth.text())
                    bdw = bdw
                except:
                    print ("# Check Bead Core Width")
                    bdw = 0.0
                    return 
                try: 
                    dRW = float(self.lineEdit_DesignRW.text())
                    dRW = dRW
                except:
                    print ("# Check PCI RW")
                    dRW = 0.0
                    return 

                if self.patternmesh =='':       kerfContact =0 
                else:                           kerfContact =1 

                if self.checkBox.isChecked() :    PCI = 1 
                else: PCI = 0

                Dialog = QtWidgets.QDialog()
                dlg = SMART.Ui_Dialog(self.materialDir, self.localCordDB, self.fullmeshSave, self.layout.GD,\
                    PCIPress, bsd, bdw, dRW, self.fileListFile, self.ISLM_cordDBFile, kerfContact, PCI, meshfile=self.layoutmesh)
                dlg.setupUi(Dialog, PCIPress)
                Dialog.exec_()
            # except:
            #     print ("## You Should generate 3D Full meshes")
        else:
            print("## You should create 3D mesh.")

    def _append_text(self, msg):
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)
        self.textBrowser.insertPlainText(msg)
        QtWidgets.QApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", self.mainWindowName))
        # MainWindow.setWindowIcon(QtGui.QIcon('tire.ico'))
        
        self.btn_auto.setText(_translate("MainWindow", "Fully automatic generation"))
        self.btn_auto.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.btn_auto.setToolTip("Shortcut to Auto-generate: Ctrl+F")

        self.sectorno.setText(_translate("MainWindow", "Sector"))
        self.input_layout_sector.setText(_translate("MainWindow", "240"))
        self.pitchno.setText(_translate("MainWindow", "Pitch"))
        self.input_pitch_no.setText(_translate("MainWindow", "0"))
        
        self.btn_layoutmesh.setText(_translate("MainWindow", "Layout mesh"))
        self.btn_layoutmesh.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.btn_layoutmesh.setToolTip("Shortcut to Layout open: Ctrl+L")

        self.btn_patternmesh.setText(_translate("MainWindow", "Pattern mesh"))
        self.btn_patternmesh.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.btn_patternmesh.setToolTip("Shortcut to Pattern open: Ctrl+P")

        self.layoutfile.setText(_translate("MainWindow", ".."))
        self.patternfile.setText(_translate("MainWindow", ".."))

        self.ABAQUS.setText(_translate("MainWindow", "ABQ"))
        self.check_T3DM.setText(_translate("MainWindow", "T3DM"))
        self.check_FricView.setText(_translate("MainWindow", "FricV"))
        self.check_SubTread.setText(_translate("MainWindow", "Sub TD"))
        self.check_Direction.setText(_translate("MainWindow", "Rot."))
        
        self.btn_removetread.setText(_translate("MainWindow", "Remove tread"))
        self.btn_removetread.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.btn_removetread.setToolTip("Shortcut to Remove: Ctrl+R")

        self.btn_expansion.setText(_translate("MainWindow", "Expand pattern"))
        self.btn_expansion.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.btn_expansion.setToolTip("Shortcut to Expand: Ctrl+E")

        self.btn_generation.setText(_translate("MainWindow", "Generate 3D"))
        self.btn_generation.setShortcut(_translate("MainWindow", "Ctrl+G"))
        self.btn_generation.setToolTip("Shortcut to Generate: Ctrl+G")

        self.groupbox_layout.setTitle(_translate("MainWindow", "View Layout                        "))
        self.radio_currentlayout.setText(_translate("MainWindow", "Default"))
        self.radio_layout.setText(_translate("MainWindow", "Layout"))
        self.radio_untreaded.setText(_translate("MainWindow", "Crown removed"))
        self.checkBox_No.setText(_translate("MainWindow", "No."))
        self.groupbox_patternstatus.setTitle(_translate("MainWindow", "Pattern Status"))
        self.radio_model.setText(_translate("MainWindow", "Model"))
        self.radio_scaled.setText(_translate("MainWindow", "Scaled"))
        self.radio_gauged.setText(_translate("MainWindow", "Gauged"))
        self.radio_bended.setText(_translate("MainWindow", "Bended"))
        self.radio_expanded.setText(_translate("MainWindow", "Expanded"))
        self.Horizontal_radio.setTitle(_translate("MainWindow", "View Pattern Surface                     "))
        self.radioDefault.setText(_translate("MainWindow", "Default"))
        self.radioTop.setText(_translate("MainWindow", "Top"))
        self.radioBottom.setText(_translate("MainWindow", "Bottom"))
        self.checkBox_SurfNo.setText(_translate("MainWindow", "No."))
        self.radioPitch.setText(_translate("MainWindow", "Pitch Up/Down"))
        self.radioSide.setText(_translate("MainWindow", "Pattern Side"))
        self.groupBox_OverlaySurf.setTitle(_translate("MainWindow", "View over pattern             "))
        self.radio_Maingrv.setText(_translate("MainWindow", "Main groove"))
        self.radio_Subgrv.setText(_translate("MainWindow", "Sub groove"))
        self.radio_Kerf.setText(_translate("MainWindow", "Kerf"))
        self.radio_AllSide.setText(_translate("MainWindow", "All kerf/Grv sides"))
        self.SearchElement.setText(_translate("MainWindow", "Show elements"))
        self.searchno.setText(_translate("MainWindow", ""))
        self.checkBox_OverlaySurfNo.setText(_translate("MainWindow", "No."))
        
        self.btn_showsolid.setText(_translate("MainWindow", "Show"))
        self.btn_showsolid.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.btn_showsolid.setToolTip("Shortcut to show: Ctrl+S")

        self.btn_PtnNodeCheck.setText(_translate("MainWindow", "pattern Mesh check(length,Jacobian)"))
        self.btn_PtnNodeCheck.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.btn_PtnNodeCheck.setToolTip("Shortcut to Mesh check: Ctrl+M")

        self.btn_initialization.setText(_translate("MainWindow", "Initilization"))
        self.btn_initialization.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.btn_initialization.setToolTip("Shortcut to Initialize: Ctrl+I")


        self.materialDirFile = "ISLM_materialDirectory.dat"
        if not isfile(self.materialDirFile):
            self.materialDir = "/home/fiper/ISLM_MAT"
            self.AngleBT1 = str(0)
            self.AngleBT2 = str(0)
            self.AngleBT3 = str(0)
            self.AngleBT4 = str(0)
            self.PCIPress = "0"

            self.WriteMaterialDirectory(self.materialDir, self.AngleBT1, self.AngleBT2, self.AngleBT3, self.AngleBT4, self.PCIPress)
            
        with open(self.materialDirFile) as MD: 
            lines = MD.readlines()

        self.materialDir = lines[0].strip()
        angles = lines[1].split(",")
        self.AngleBT1 = angles[0].strip()
        self.AngleBT2 = angles[1].strip()
        self.AngleBT3 = angles[2].strip()
        self.AngleBT4 = angles[3].strip()
        self.PCIPress =  lines[2].strip()

        self.label_bt1.setText(_translate("MainWindow", "Angle BT1"))
        self.lineEdit_bt1.setText(_translate("MainWindow", self.AngleBT1))
        self.label_bt2.setText(_translate("MainWindow", "BT2"))
        self.lineEdit_bt2.setText(_translate("MainWindow", self.AngleBT2))
        self.label_bt3.setText(_translate("MainWindow", "BT3"))
        self.lineEdit_bt3.setText(_translate("MainWindow", self.AngleBT3))
        self.label_bt4.setText(_translate("MainWindow", "BT4"))
        self.lineEdit_bt4.setText(_translate("MainWindow", self.AngleBT4))

        # self.message.setText(_translate("MainWindow", ".."))
        
        
        self.lineEdit_materialDir.setText(_translate("MainWindow", self.materialDir))


        self.checkBox.setText(_translate("MainWindow", "PCI"))
        # self.line_PCI_Press.setText(_translate("MainWindow", "2.0"))
        self.line_PCI_Press.setText(_translate("MainWindow", self.PCIPress))
        self.checkBox_overType.setText(_translate("MainWindow", "TBR : Tread Over Side"))
        self.label_bt1.setText(_translate("MainWindow", "Angle BT1"))
        # self.lineEdit_bt1.setText(_translate("MainWindow", "0"))
        self.label_bt2.setText(_translate("MainWindow", "BT2"))
        # self.lineEdit_bt2.setText(_translate("MainWindow", "0"))
        self.label_bt3.setText(_translate("MainWindow", "BT3"))
        # self.lineEdit_bt3.setText(_translate("MainWindow", "0"))
        self.label_bt4.setText(_translate("MainWindow", "BT4"))
        # self.lineEdit_bt4.setText(_translate("MainWindow", "0"))
        self.label_BSD.setText(_translate("MainWindow", "BSD"))
        self.lineEdit_BSD.setText(_translate("MainWindow", "0"))
        self.label_BDWidth.setText(_translate("MainWindow", "BD Width"))
        self.lineEdit_BDWidth.setText(_translate("MainWindow", "0"))
        self.label_DesignRW.setText(_translate("MainWindow", "PCI RW"))
        self.lineEdit_DesignRW.setText(_translate("MainWindow", "0"))



        self.btn_material.setText(_translate("MainWindow", "Update material DB"))
        self.btn_material.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.btn_material.setToolTip("Shortcut to Quit: Ctrl+U")

    def Generate_Rotated_PTN(self): 
        if self.readpattern:  
            savefile, _= QtWidgets.QFileDialog.getSaveFileName(None, "Save files as",self.patternmesh[:-4]+"-Reversed.ptn" , "Pattern Mesh(*.ptn)")
            if savefile: PTN.Generate_Rotated_PTN(self.patternmesh, savefile)
        else: 
            pass 


    def ptn_checking(self): 
        
        if self.readpattern: 
            dups = []
            margin = 0.1E-03
            # solids = self.ptn_model.nps 
            if self.radio_model.isChecked() : 
                nodes = self.ptn_model.npn
                solids = self.ptn_model.nps 
            elif self.radio_scaled.isChecked() : 
                nodes = self.ptn_expanded.npn
                solids = self.ptn_expanded.nps
            elif self.radio_gauged.isChecked() : 
                nodes = self.ptn_gauged.npn
                solids = self.ptn_gauged.nps
            elif self.radio_bended.isChecked() : 
                nodes = self.ptn_bended.npn
                solids = self.ptn_bended.nps
            elif self.radio_expanded.isChecked() : 
                nodes = self.ptn_bottomed.npn
                solids = self.ptn_bottomed.nps
            else : 
                nodes = self.pattern.npn
                solids = self.ptn_model.nps 
                
            PTN.PatternElementDuplicationCheck(solids)
            
            NodesInSolid=PTN.SearchingNodesInElement(nodes, solids)
            if len(NodesInSolid): 
                for ns in NodesInSolid: 
                    txt = ""
                    for n in ns[1]: 
                        txt+= str(int(n))+", "
                    txt=txt[:-2]
                    print (" %s in Element %d"%(txt, ns[0]))
            
            cnt, cln = PTN.NodeDistanceChecking(nodes, solids, margin=margin)
            if cnt > 0: 
                dupn = []
                txt = "* %d nodes are close under %.2fmm\n"%(cnt, margin*1000)
                cnt = 0 
                for cn in cln : 
                    
                    for i, tx in enumerate(cn): 
                        
                        if i ==0: 
                            txt += "Cases %d\n"%(cnt+1)
                            txt += "%6d,%7.2f,%7.2f,%7.2f\n"%(tx[0]-10**7, tx[1]*1000, tx[2]*1000, tx[3]*1000) 
                            if cnt ==0: dupn.append(tx[0])
                        else: 
                            if tx[0][0] != cn[0][0]:
                                txt += "%6d,%7.2f,%7.2f,%7.2f (%.2fmm)\n"%(tx[0][0]-10**7, tx[0][1]*1000, tx[0][2]*1000, tx[0][3]*1000, tx[1]*1000)
                                if cnt == 0: dupn.append(tx[0][0])
                    cnt += 1 
                
                for dn in dupn: 
                    idx = np.where(solids[:,1:9]==dn)[0]
                    for ix in idx: 
                        dups.append(solids[ix])
                if len(dups) > 0: 
                    self.figure.plot_error(dups, nodes)
                    self.ShowingImage = '3D'
            else: 
                txt = "* All nodes Distances are over %.2fmm\n"%(margin*1000)

            self._append_text(txt)
                
            errel, jac_message, negative_ht,_ = PTN.Jacobian_check(nodes, solids)

            if len(dups) == 0 and len(errel) > 0 : 
                print ("## Elements need to check ")
                for el in errel:
                    print(int(el[0]), end=", ")
                self.figure.plot_error(errel, nodes)
                self.ShowingImage = '3D'

    def exiting(self): 
        self.Initilize()
        sys.exit()

    def WriteMaterialDirectory(self, directory, bt1, bt2, bt3, bt4, pciPress): 
        f=open(self.materialDirFile, 'w')
        f.write("%s\n"%(directory))
        f.write("%s, %s, %s, %s\n"%(bt1, bt2, bt3, bt4))
        f.write("%s\n"%(pciPress))
        f.close()
    def ChangeBTAngle(self, fname): 
        # with open(fname) as DB: 
        #     lines = DB.readlines()
        savefile = fname[:-13]

        self.AngleBT1=self.lineEdit_bt1.text()
        self.AngleBT2=self.lineEdit_bt2.text()
        self.AngleBT3=self.lineEdit_bt3.text()
        self.AngleBT4=self.lineEdit_bt4.text()
        self.PCIPress=self.line_PCI_Press.text()
        BT_angles=[float(self.AngleBT1), float(self.AngleBT2), float(self.AngleBT3), float(self.AngleBT4)]
        if self.checkBox_overType.isChecked(): overtype = "TOS"
        else:  overtype = "SOT"
        if savefile !="": 
            PTN.SmartMaterialInput(axi=savefile +".axi", trd=savefile +".trd", layout=self.layoutmesh, \
                elset=self.layout.Elset.Elset, node=self.layout.Node.Node, element=self.layout.Element.Element,\
                        materialDir=self.materialDir, btAngles=BT_angles, \
                            overtype=overtype, PCIPress=self.PCIPress, bdw=self.layout.beadWidth*1000, pattern=self.readpattern)

                
    def Update_ISLM_Material(self): 
        self.materialDir = self.lineEdit_materialDir.text()
        try:
            data = float(self.lineEdit_bt1.text())
        except:
            print(" # Check the Angle of #1 Belt")
            return 
        try:
            data = float(self.lineEdit_bt2.text())
        except:
            print(" # Check the Angle of #2 Belt")
            return 
        try:
            data = float(self.lineEdit_bt3.text())
        except:
            print(" # Check the Angle of #3 Belt")
            return 
        try:
            data = float(self.lineEdit_bt4.text())
        except:
            print(" # Check the Angle of #4 Belt")
            return 
        try:
            data = float(self.line_PCI_Press.text())
        except:
            print(" # Check PCI Pressure")
            return 
        self.AngleBT1=self.lineEdit_bt1.text()
        self.AngleBT2=self.lineEdit_bt2.text()
        self.AngleBT3=self.lineEdit_bt3.text()
        self.AngleBT4=self.lineEdit_bt4.text()
        self.PCIPress=self.line_PCI_Press.text()
        

        self.WriteMaterialDirectory(self.materialDir, self.AngleBT1, self.AngleBT2, self.AngleBT3, self.AngleBT4, self.PCIPress)

        
        
        matFile = self.fullmeshSave + "-material.dat"
        self.ChangeBTAngle(matFile)
        host = "None"; user='None'
        try: 
            with open(self.materialDBfilename) as DB : 
                lines = DB.readlines()
            host = lines[0].strip()
            user = lines[1].strip()
            pw = lines[2].strip()
        except:
            print ("\n## No Information for log-in to DB")
            print ("   Please register. (INP/Register DB)")
            print ("## Current IP:", host)
            print ("## User:", user)
            return 
        try : 
            success = PTN.Update_ISLM_Material(wdir=self.materialDir,  cordSaveFile=self.localCordDB, fileListFile=self.fileListFile, \
                host=host, user=user, pw=pw, cordfile=self.ISLM_cordDBFile)
            if success ==1:     print ("\n* Mateiral DB was updated.")
            else: print ("## cannot access to server")
           
            # print ("* ISLM Mateiral DB was updated.")
        except:
            print ("## Cannot access Mateiral DB.")
            print ("## Check the connection to DB")
            print ("## Current IP:", host)
            print ("## User:", user)
        
    def FricView_Checking(self): 
        if self.check_FricView.isChecked() == True: 
            writestatus(negSho=1)
        else: 
            writestatus(negSho=0)


    def T3DM_Checking(self): 
        try: 
            if self.check_T3DM.isChecked() == True : 
                self.layout.T3DMMODE = 1 
            else: 
                self.layout.T3DMMODE = 0 
        except:
            pass 

        if self.check_T3DM.isChecked() == True : 
            writestatus(T3DM=1)
        else: 
            writestatus(T3DM=0)

        if self.readpattern == 1 and self.readlayout == 1: 
            if self.layout.TDW > 0 and self.pattern.TreadDesignWidth: 
                RecPL = self.layout.TDW / self.pattern.TreadDesignWidth * self.pattern.pitchlength
            else: 
                RecPL = self.pattern.pitchlength
            if self.check_T3DM.isChecked() == True: 
                RecPL = self.pattern.pitchlength
            PN = round(self.layout.OD * self.PI / RecPL , 0)
            NoPitch = int(PN)
            self.input_pitch_no.setText(str(NoPitch))

    def SUT_Checking(self): 
        if self.check_SubTread.isChecked() == True: 
            writestatus(SUT=1)
        else: 
            writestatus(SUT=0)

    def ABAQUS_Checking(self): 
        if self.ABAQUS.isChecked() == True: 
            writestatus(ABQ=1)
        else: 
            writestatus(ABQ=0)


    def PTN_Direction_Change(self): 
        if self.readpattern: 
            rot =radians(180.0)
            for i, npn in enumerate(self.pattern.npn) :
                self.pattern.npn[i] = PTN.RotateNode(npn, angle=rot, xy=21)

            tempSurf = []
            for sf in self.pattern.surf_pitch_up: 
                tempSurf.append(sf)
            tempSf = []
            for sf in self.pattern.surf_pitch_down: 
                tempSf.append(sf)

            self.pattern.surf_pitch_up = np.array(tempSf)
            self.pattern.surf_pitch_down = np.array(tempSurf)


            tempSurf = []
            for sf in self.pattern.surf_pattern_neg_side: 
                tempSurf.append(sf)
            tempSf = []
            for sf in self.pattern.surf_pattern_pos_side: 
                tempSf.append(sf)

            self.pattern.surf_pattern_neg_side = np.array(tempSf)
            self.pattern.surf_pattern_pos_side = np.array(tempSurf)


            # self.figure.plot(pattern=self.pattern, show='pattern')
            # self.ShowingImage = 'pattern'

            print ("************************************")
            print ("** Pattern was ROTATED.")
            print ("************************************")

            return 

            for npn in self.pattern.npn : 
                npn[1] = OP_mul(npn[1], -1.0)
            
            N = len(self.pattern.nps)

            for i in range(N): 
                if self.pattern.nps[i][7] > 0: 

                    t1 = self.pattern.nps[i][1]; t2 = self.pattern.nps[i][2]; t3 = self.pattern.nps[i][3]; t4=self.pattern.nps[i][4]
                    self.pattern.nps[i][1] = t4; self.pattern.nps[i][2]= t3; self.pattern.nps[i][3] = t2; self.pattern.nps[i][4] = t1 

                    t1 = self.pattern.nps[i][5]; t2 = self.pattern.nps[i][6]; t3 = self.pattern.nps[i][7]; t4=self.pattern.nps[i][8]
                    self.pattern.nps[i][5] = t4; self.pattern.nps[i][6]= t3; self.pattern.nps[i][7] = t2; self.pattern.nps[i][8] = t1 

                else: 

                    t2 = self.pattern.nps[i][2]; t3 = self.pattern.nps[i][3]
                    self.pattern.nps[i][2] = t3; self.pattern.nps[i][3]= t2

                    t2 = self.pattern.nps[i][5]; t3 = self.pattern.nps[i][6]
                    self.pattern.nps[i][5] = t3; self.pattern.nps[i][6]= t2

            for k, sf in enumerate(self.pattern.surf_pitch_up): 
                if sf[1]>2:
                    t1 = sf[7]; sf[7] = sf[8]; sf[8]=t1 
                    t1 = sf[9]; sf[9] = sf[10]; sf[10]=t1
                    # if sf[1] ==3: sf[1]==5
                    # elif sf[1] ==5: sf[1]==3
                    self.pattern.surf_pitch_up[k]=sf 
            for k, sf in enumerate(self.pattern.surf_pitch_down):  
                if sf[1]>2:
                    t1 = sf[7]; sf[7] = sf[8]; sf[8]=t1 
                    t1 = sf[9]; sf[9] = sf[10]; sf[10]=t1
                    # if sf[1] ==3: sf[1]==5
                    # elif sf[1] ==5: sf[1]==3
                    self.pattern.surf_pitch_down[k]=sf 
            for k, sf in enumerate(self.pattern.surf_pattern_neg_side): 
                if sf[1]>2:
                    t1 = sf[7]; sf[7] = sf[8]; sf[8]=t1 
                    t1 = sf[9]; sf[9] = sf[10]; sf[10]=t1
                    # if sf[1] ==3: sf[1]==5
                    # elif sf[1] ==5: sf[1]==3
                    self.pattern.surf_pattern_neg_side[k]=sf 
            for k, sf in enumerate(self.pattern.surf_pattern_pos_side): 
                if sf[1]>2:
                    t1 = sf[7]; sf[7] = sf[8]; sf[8]=t1 
                    t1 = sf[9]; sf[9] = sf[10]; sf[10]=t1
                    # if sf[1] ==3: sf[1]==5
                    # elif sf[1] ==5: sf[1]==3
                    self.pattern.surf_pattern_pos_side[k]=sf 
            for k, sf in enumerate(self.pattern.PTN_AllFreeSurface): 
                if sf[1]>2:
                    t1 = sf[7]; sf[7] = sf[8]; sf[8]=t1 
                    t1 = sf[9]; sf[9] = sf[10]; sf[10]=t1
                    # if sf[1] ==3: sf[1]==5
                    # elif sf[1] ==5: sf[1]==3
                    self.pattern.PTN_AllFreeSurface[k]=sf 
            for k, sf in enumerate(self.pattern.freebottom): 
                if sf[1]>2:
                    t1 = sf[7]; sf[7] = sf[8]; sf[8]=t1 
                    t1 = sf[9]; sf[9] = sf[10]; sf[10]=t1
                    # if sf[1] ==3: sf[1]==5
                    # elif sf[1] ==5: sf[1]==3
                    self.pattern.freebottom[k]=sf 

            #  surf_pitch_up, surf_pitch_down, surf_free=[], surf_btm=[], surf_side=[],
            # self.pattern.PTN_AllFreeSurface, self.pattern.freebottom,
            for bm in self.pattern.UpBack: 
                bm[3][0] *= -1 
                bm[4][0] *= -1 


            self.figure.plot(pattern=self.pattern, show='pattern')
            self.ShowingImage = 'pattern'

            print ("************************************")
            print ("** Pattern direction was reversed.")
            print ("************************************")


    def Initilize(self): 

        try: 
            Mesh2DInp = self.layoutmesh[:-4] + "-tmp.tmp"
            remove(Mesh2DInp)
        except: 
            pass 
            
        try: 
            remove("currentSmartInput.tmp")
        except: 
            pass

        try:   del(self.pattern)
        except: pass 
        try: del(self.layout)
        except: pass 
        self.input_pitch_no.setEnabled(True)
        self.input_layout_sector.setEnabled(True)

        self.input_pitch_no.setText("0")
        # self.input_layout_sector.setText("240")
        self.layoutfile.setText("")
        self.patternfile.setText("")
        try: del(self.ptnnode)
        except: pass
        try: del(self.ptnsolid)
        except: pass
        try: del(self.laytie)
        except: pass
        try: del(self.txtelset)
        except: pass
        try: del(self.poffset)
        except: pass
        self.btn_removetread.setDisabled(True)
        self.btn_expansion.setDisabled(True)
        self.btn_generation.setDisabled(True)
        self.btn_layoutmesh.setEnabled(True)
        self.btn_patternmesh.setEnabled(True)
        self.radioDefault.setChecked(True)

        self.fullmeshSave = ''
        self.patternmesh=''
        

        try: del(self.ptn_model)
        except: pass
        try: del(self.ptn_expanded)
        except: pass
        try: del(self.ptn_gauged)
        except: pass
        try: del(self.ptn_bended)
        except: pass
        try: del(self.ptn_bottomed)
        except: pass

        try: del(self.UntreadedLayout)
        except: pass
        try: del(self.InitialLayout)
        except: pass 

        self.radio_model.setChecked(True)
        self.LayoutNo = 0 
        self.checkBox_No.setChecked(False)
        self.checkBox_SurfNo.setChecked(False)
        self.radio_currentlayout.setChecked(True)
        self.searchno.setText("")
        
        self.filesaved =0
        self.treadremoved = 0  
        self.patternexpanded = 0 
        self.readlayout = 0;         self.readpattern = 0 

        self.P3DMLayout = 0 
        self.P3DMPattern = 0 

        # self.check_T3DM.setChecked(False)
        # self.check_Direction.setChecked(False)
        self.check_T3DM.setEnabled(True)
        
        self.check_Direction.setEnabled(True)
        self.check_SubTread.setEnabled(True)
        # self.check_FricView.setEnabled(True) 
        # self.check_FricView.setChecked(False)

        self.textBrowser.clear()
        self.figure.plot(show='none') 
        self.ShowingImage = 'none'
        # self.message.setText("Ready for another mesh generation")
        

    def autogeneration(self): 
        self.Initilize()
        self.patternmesh = ""
        self.fullmeshSave=''
        self.filesaved = 0
        self.treadremoved = 0  
        self.patternexpanded = 0 
        self.radioDefault.setChecked(True)

        self.check_T3DM.setEnabled(True)
        self.checkBox_SurfNo.setChecked(False)
        

        try: 
            Mesh2DInp = self.layoutmesh[:-4] + "-tmp.tmp"
            remove(Mesh2DInp)
        except: 
            pass 


        # self.message.setText("Please Select Tire Layout mesh file (2D)")
        self.layoutmesh, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select layout mesh File", self.cwd, "Layout Mesh(*.inp)") 
        if self.layoutmesh : 
            if '/' in self.layoutmesh: self.layoutms = self.layoutmesh.split("/")[-1].split(".")[0]
            else: self.layoutms = self.layoutmesh.split("\\")[-1].split(".")[0]
            self.layoutfile.setText(self.layoutms)
            self.cwd=writeworkingdirectory(self.layoutmesh, dfile=self.dfile)
            self.savedirectory = self.cwd 
        else: 
            hwnd = win32gui.FindWindow(None, self.mainWindowName)
            win32gui.SetForegroundWindow(hwnd)
            return 
        
        # self.message.setText("Please Select 3D Pattern mesh file")
        self.patternmesh, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select pattern mesh File", self.cwd, "Pattern Mesh(*.ptn)") 
        
        if self.patternmesh: 
            if '/' in self.patternmesh: self.ptnms = self.patternmesh.split("/")[-1].split(".")[0]
            else: self.ptnms = self.patternmesh.split("\\")[-1].split(".")[0]
            self.patternfile.setText(self.ptnms)
            self.cwd=writeworkingdirectory(self.patternmesh, dfile=self.dfile)
        else:
            self.layoutfile.setText("")
            hwnd = win32gui.FindWindow(None, self.mainWindowName)
            win32gui.SetForegroundWindow(hwnd)
            return 

        self.input_pitch_no.setText("0")
        self.user_sector=int(self.input_layout_sector.text()) 

        hwnd = win32gui.FindWindow(None, self.mainWindowName)
        win32gui.SetForegroundWindow(hwnd)

        if self.patternmesh and self.layoutmesh: 
            
            
            self.patternfile.setText(self.ptnms)
            self.layoutfile.setText(self.layoutms)

            errors = 0 
            L_profile, R_profile, OD, TW, TDW, GD = PTN.ReadMoldProfileFromPatternMeshFile(self.patternmesh)

            opened = self.read_layout()
            if opened == 0: 
                print (" ## Please Restart.")
                self.btn_layoutmesh.setDisabled(True)
                self.btn_patternmesh.setDisabled(True)
                return 
            # t0 = time()
            opened = self.read_pattern()
            # t1 = time()
            # print ("READ PTN %.2f"%(t1-t0))
            # return 
            if opened == 0: 
                print (" ## Please Restart.")
                self.btn_layoutmesh.setDisabled(True)
                self.btn_patternmesh.setDisabled(True)
                return 
            self.reversed_pattern = -1 

            if self.check_T3DM.isChecked() == True :      self.layout.T3DMMODE = 1 
            else:                                         self.layout.T3DMMODE = 0 

            if self.pattern.TreadDesignWidth==0:     return 

            self.removal_tread()
            self.expansion_ptn()

            self.generation_mesh()
            self.btn_layoutmesh.setDisabled(True)
            self.btn_patternmesh.setDisabled(True)
            return 

        elif self.patternmesh: 
            self.Initilize()
            self.open_pattern()
            # self.message.setText("Layout mesh file is not opened")
            self.cwd=writeworkingdirectory(self.patternmesh, dfile=self.dfile)
        elif self.layoutmesh: 
            self.Initilize()
            self.open_layout()
            # self.message.setText("Pattern mesh file is not opened")
            self.cwd=writeworkingdirectory(self.layoutmesh, dfile=self.dfile)
        else:
            # self.message.setText("Pattern / layout mesh files are not opened")
            pass

    def read_layout(self): 
        if '/' in self.layoutmesh: self.layoutms = self.layoutmesh.split("/")[-1].split(".")[0]
        else: self.layoutms = self.layoutmesh.split("\\")[-1].split(".")[0]
        self.layoutfile.setText(self.layoutms)
        self.cwd=writeworkingdirectory(self.layoutmesh, dfile=self.dfile)
        self.savedirectory = self.cwd 
        try:      del(self.layout)
        except:   pass
        # self.message.setText(self.layoutmesh)
        self.P3DMLayout = 0 
        with open(self.layoutmesh) as LM: 
            lines = LM.readlines()
        self.lineEdit_DesignRW.setText("0")
        self.lineEdit_BSD.setText("0")
        self.lineEdit_BDWidth.setText("0")
        for i, line in enumerate(lines): 
            if "LAYOUT RIM WIDTH" in line and "**" in line: 
                data = line.split(":")[1].strip()
                self.lineEdit_DesignRW.setText(data)
            if "BEAD SET DISTANCE" in line and "**" in line: 
                data = float(line.split(":")[1].strip())
                data = "%.1f"%(data)
                self.lineEdit_BSD.setText(data)
            if i < 100: 
                if "TREAD REMOVED LAYOUT MESH BY P3DM" in line: 
                    print ("* The mesh without tread was generated by P3DM")
                    self.P3DMLayout = 1 
                    break 
            else: 
                break 
        
        self.layout = PTN.MESH2D(self.layoutmesh)
        self.lineEdit_BDWidth.setText(str(round(self.layout.beadWidth*1000,2)))
        try: 
            if len(self.layout.Tread.Element) == 0 and self.layout.T3DMMODE : 
                self.layout.OD = self.pattern.diameter
                self.layout.TDW = self.pattern.TreadDesignWidth
                self.layout.GD = self.pattern.ModelGD 
                # print ("TIRE OD =%.2f"%(self.layout.OD*1000))
        except:
            pass 

        if self.layout.IsError == 100: 
            del(self.layout)
            return 0
        elif self.layout.IsError  > 0: 
            self.figure.plot(layout=self.layout, show='layout', add2d=self.layout.TieError) 
            self.ShowingImage = 'layout'
            del(self.layout)
            # self.btn_layoutmesh.setEnabled(True)
            # self.btn_patternmesh.setDisabled(True)
            return 0
        else: 
            if self.P3DMLayout == 0: 
                if self.layout.T3DMMODE == 1: 
                    self.check_T3DM.setChecked(True)
                    self.check_T3DM.setEnabled(False)
                    
                self.InitialLayout = PTN.COPYLAYOUT(self.layout)
                self.btn_layoutmesh.setDisabled(True)
                self.figure.plot(layout=self.layout, show='layout', add2d=self.layout.TieError) 
                self.ShowingImage = 'layout'
                self.readlayout = 1

                # if self.layout.shoulderType =='S':   self.btn_removetread.setEnabled(True)

                if self.readpattern == 1: 
                    if self.layout.TDW > 0 and self.pattern.TreadDesignWidth: 
                        RecPL = self.layout.TDW / self.pattern.TreadDesignWidth * self.pattern.pitchlength
                    else: 
                        RecPL = self.pattern.pitchlength
                    if self.check_T3DM.isChecked() == True: 
                        RecPL = self.pattern.pitchlength
                    PN = round(self.layout.OD * self.PI / RecPL , 0)
                    NoPitch = int(PN)
                    self.input_pitch_no.setText(str(NoPitch))
                    self.btn_removetread.setEnabled(True)
                    self.btn_expansion.setEnabled(True) 
                    self.default_pitch = NoPitch 
                    self.btn_generation.setEnabled(True)

                    if self.pattern.shoulderType == "S" : 
                        if self.layout.shoulderType == "R": print ("* Shoulder type changed to SQUARE")
                        self.layout.shoulderType = "S"
                return 1 
            else: 
                self.figure.plot(layout=self.layout, show='layout', add2d=self.layout.TieError) 
                self.ShowingImage = 'layout'
                return 0 

    def open_layout(self): 
        try: 
            Mesh2DInp = self.layoutmesh[:-4] + "-tmp.tmp"
            remove(Mesh2DInp)
        except: 
            pass
        if self.P3DMLayout == 1: 
            try: 
                del(self.layout)
            except: 
                pass 
            self.P3DMLayout = 0 

        self.layoutmesh, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select layout mesh File", self.cwd, "File(*.inp)") 
        if self.layoutmesh: 
            self.radioDefault.setChecked(True)
            opened = self.read_layout()
            if opened == 0: 
                print ("## Select a layout mesh")
            elif self.readpattern == 0: 
                self.btn_generation.setEnabled(True)
        return 

    def read_pattern (self): 
        if '/' in self.patternmesh: self.ptnms = self.patternmesh.split("/")[-1].split(".")[0]
        else: self.ptnms = self.patternmesh.split("\\")[-1].split(".")[0]
        self.patternfile.setText(self.ptnms)

        self.cwd=writeworkingdirectory(self.patternmesh, dfile=self.dfile)
        # self.message.setText(self.layoutmesh)

        try: del(self.pattern)
        except: pass 

        self.P3DMPattern = 0 
        with open(self.patternmesh) as LM: 
            lines = LM.readlines()
        for i, line in enumerate(lines): 
            if i < 100: 
                if "Regenerated Pattern mesh from P3DM" in line: 
                    self.P3DMPattern = 1 
                    break 
            else:
                break 

        if self.P3DMPattern == 0: 
            # t0 = time()
            self.pattern = PTN.PATTERN(self.patternmesh, test=0)

            if self.pattern.TreadDesignWidth==0: 
                print ("\n********************************************")
                print (" Tread Design Width is not in the pattern mesh.")
                print (" Insert 'Tread Design Width' into *.ptn")
                print ("*TREAD_DESIGN_WIDTH : OOO.OO")
                print ("********************************************\n")
                return 

            try: 
                if len(self.layout.Tread.Element) == 0 and self.layout.T3DMMODE : 
                    self.layout.OD = self.pattern.diameter
                    self.layout.TDW = self.pattern.TreadDesignWidth
                    self.layout.GD = self.pattern.ModelGD 
                    # print ("TIRE OD =%.2f"%(self.layout.OD*1000))
            except:
                pass 

            if self.pattern.IsError ==1: 
                return 0 
            self.radio_model.setChecked(True)
            self.ptn_model = PTN.COPYPTN(self.pattern)
            NN = len(self.pattern.npn); NS= len(self.pattern.nps)
            # print ("* Pattern nodes=%d, elements=%d\n"%(NN, NS))
            self.figure.plot(pattern=self.pattern, show='pattern')
            self.ShowingImage = 'pattern'
            self.btn_patternmesh.setDisabled(True)
            self.readpattern = 1
            

            if len(self.pattern.errsolid) > 0: 
                print (self.pattern.errsolid)
                for sd in self.pattern.errsolid: 
                    print (" Distored %d"%(sd[0]))
                self.figure.plot_error(self.pattern.errsolid, self.pattern.npn)
                self.ShowingImage = '3D'
                return 0
            elif self.pattern.errorcode != 0 : 
                self.figure.plot_error(self.pattern.errorcode, self.pattern.npn)
                self.ShowingImage = '3D'
                return 0 
            else: 
                if self.readlayout == 1: 
                    if self.layout.TDW > 0 and self.pattern.TreadDesignWidth: 
                        RecPL = self.layout.TDW / self.pattern.TreadDesignWidth * self.pattern.pitchlength
                    else: 
                        RecPL = self.pattern.pitchlength
                    if self.check_T3DM.isChecked() == True: 
                        RecPL = self.pattern.pitchlength
                    PN = round(self.layout.OD * self.PI / RecPL , 0)

                    NoPitch = int(PN)
                    self.input_pitch_no.setText(str(NoPitch))
                    self.btn_expansion.setEnabled(True) 
                    if self.treadremoved ==0: self.btn_removetread.setEnabled(True)
                    self.default_pitch = NoPitch 
                        
                    if self.pattern.shoulderType == "S" : 
                        if self.layout.shoulderType == "R": print ("* Shoulder type changed to SQUARE")
                        self.layout.shoulderType = "S"


                return 1 
        else: 
            print ("* This pattern mesh was generated by P3DM")
            print ("            already bent to filt a layout")
            return 0  

    def open_pattern(self): 
        
        if self.P3DMPattern == 1: 
            try: 
                del(self.pattern)
            except: 
                pass 
            self.P3DMPattern = 0 

        self.radioDefault.setChecked(True)
        
        self.patternmesh, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select pattern mesh File", self.cwd, "File(*.ptn)") 
        
        if self.patternmesh: 
            
            if '/' in self.patternmesh: self.ptnms = self.patternmesh.split("/")[-1].split(".")[0]
            else: self.ptnms = self.patternmesh.split("\\")[-1].split(".")[0]
            self.patternfile.setText(self.ptnms)

            self.cwd=writeworkingdirectory(self.patternmesh, dfile=self.dfile)
            # self.message.setText(self.layoutmesh)

            try: del(self.pattern)
            except: pass 

            opened = self.read_pattern()


            if opened == 0: 
                print ("## Select a pattern mesh")
                return 

            try: 
                bottomEdges=SurfaceBoundary(self.pattern.freebottom)
                edgeGroup=PTN.MakeEdgesToBlockGroup(bottomEdges)
                if len(edgeGroup)>1: 
                    print ("#########################################")
                    print ("## Bottom Surface has (a) hole(s) : %d"%(len(edgeGroup)-1))
                    print ("## Check bottom surface ")
                    print ("#########################################")
            except:
                print (" Pattern mesh is not opened.")
            
    def removal_tread(self): 
        self.radioDefault.setChecked(True)
        self.check_T3DM.setEnabled(False)

        if self.patternmesh !="" : # or self.layout.shoulderType =='S':

            if self.check_T3DM.isChecked() == True : 
                self.layout.T3DMMODE = 1 
            else: 
                self.layout.T3DMMODE = 0 

            self.check_T3DM.setEnabled(False)

            # print ("*EXPANSION MODE (1=T3DM, 0=Expd)=%d"%(self.layout.T3DMMODE))
            
            
            
            if self.layout.shoulderType == 'R':
                self.layout.EliminateTread(self.layoutmesh, self.patternmesh, self.pattern.leftprofile, self.pattern.rightprofile,\
                    self.pattern.diameter, self.pattern.TreadDesignWidth, self.pattern.PatternWidth, self.pattern.ModelGD, t3dm=self.layout.T3DMMODE, result=0, layoutProfile=self.layout.RightProfile)
            else: 
                self.layout.ElimateSquareTread(self.pattern.leftprofile, self.pattern.rightprofile)

            if self.layout.shoulderType == 'R':
                self.flattened_Tread_bottom_sorted, self.layout.GD = PTN.Unbending_layoutTread(self.layout.tdnodes, self.layout.Tread, \
                    self.layout.LeftProfile, self.layout.RightProfile, self.layout.L_curves, self.layout.R_curves, self.layout.OD, \
                    ptn_node=self.pattern.npn, GD=self.layout.GD)
                self.shoulderGa = PTN.ShoulderTreadGa(self.layout.OD, self.layout.RightProfile, self.layout.R_curves, \
                    self.flattened_Tread_bottom_sorted, self.layout.TDW, shoR=self.layout.r_shocurve)

            elif self.layout.shoulderType == 'S'  and len(self.layout.tdnodes.Node) > 0 and self.layout.T3DMMODE ==0: 
                self.flattened_Tread_bottom_sorted,   self.layout.sideNodes=PTN.Unbending_squareLayoutTread(self.layout.tdnodes, self.layout.Tread, \
                    self.layout.LeftProfile, self.layout.RightProfile, self.layout.OD, self.layout.R_curves, shoDrop=self.layout.shoulderDrop)
                self.shoulderGa = 1.0

                if len(self.flattened_Tread_bottom_sorted) ==0: return 
            
            self.check_T3DM.setEnabled(False)

            self.treadremoved = 1 
            self.btn_removetread.setDisabled(True)
            self.UntreadedLayout = PTN.COPYLAYOUT(self.layout)
            self.figure.plot(layout=self.layout, show='layout')
            self.ShowingImage = 'layout'
                # print ("* Profile Shoulder T/D Ga=%.1f, Sho. R=%.2f"%(self.shoulderGa*1000,self.layout.r_shocurve*1000))
            return 


        else: 
            line = " Need to add function that removes  'str', 'utr' elset"
            # self.message.setText(line)

        
        # if self.patternexpanded ==1: 
        #     self.btn_generation.setEnabled(True)

    def expansion_ptn(self): 
        self.radioDefault.setChecked(True)
        if self.readlayout ==1: 
            if self.treadremoved == 0:     self.removal_tread()

            self.input_pitch_no.setDisabled(True)
            self.user_number_pitch = int(self.input_pitch_no.text())
            if abs((int(self.default_pitch) - self.user_number_pitch)) > int(self.default_pitch/10): 
                print ("******************************************")
                print ("## WARNING. Number of the pitch")
                print ("## Defalut pitch=%d, your pitch=%d"%(self.default_pitch, self.user_number_pitch))
                print ("## Check the pattern shape. ")
                print ("******************************************")
            # print ("*layout TDW=%.2f (Target=%.2f)"%(self.layout.TDW*1000, self.layout.TargetPatternWidth*1000))
            if self.layout.OD ==0.0: 
                self.layout.OD = np.max(self.pattern.npn[:,3]) * 2.0

            auto_pitch=self.pattern.Expansion(self.layout.OD, self.layout.TDW, self.layout.TargetPatternWidth,\
                 self.layout.GD, user_pitch_no=self.user_number_pitch, t3dm=self.layout.T3DMMODE, shoulder=self.layout.shoulderType)

            self.input_pitch_no.setText(str(auto_pitch))
            self.patternexpanded = 1 
            self.radio_scaled.setChecked(True)
            line = "Pattern mesh is expanded."
            # self.message.setText(line)
            self.ptn_expanded = PTN.COPYPTN(self.pattern)

            


        else: 
            line = " no need to expand"
            # self.message.setText(line)

        if self.treadremoved ==1 and self.errorcode ==0 : 
            self.btn_generation.setEnabled(True)
            self.btn_expansion.setDisabled(True)

        if self.errorcode ==0: 
            self.figure.plot(pattern=self.pattern, show='pattern')
            self.ShowingImage = 'pattern'

    def generation_mesh(self): 
            
        self.radioDefault.setChecked(True)
        Mesh2DInp = self.layoutmesh[:-4] + "-tmp.tmp"
        if path.isfile (Mesh2DInp) : remove(Mesh2DInp)

        BodyStartNo = 1
        BodyOffset  = 10000
        
        self.user_sector=int(self.input_layout_sector.text()) 
        if self.user_sector < 20: 
            print ("##########################################")
            print ("## WARNING. Check Layout sectors")
            print ("## Defalut sectors=240, your sectors=%d"%(self.user_sector))
            print ("##########################################")
            

        if self.readpattern == 0: 
            filename = self.layoutms+".axi"
            savefile, _= QtWidgets.QFileDialog.getSaveFileName(None, "Save files as", self.savedirectory+"/"+filename, "Layout 3D Mesh(*.axi)")
            if savefile !='': 
                hwnd = win32gui.FindWindow(None, self.mainWindowName)
                win32gui.SetForegroundWindow(hwnd)
        
                print ("******************************************")
                print ("** Generate 3d tire mesh without pattern")
                print ("******************************************")
                
                print ("* Layout Sectors =%d (sector=%.2f degree)"%(self.user_sector, 360.0/float(self.user_sector)))

                if self.ABAQUS.isChecked() == True: 
                    abq = 1
                else:
                    abq = 0 
                
                self.AngleBT1=self.lineEdit_bt1.text()
                self.AngleBT2=self.lineEdit_bt2.text()
                self.AngleBT3=self.lineEdit_bt3.text()
                self.AngleBT4=self.lineEdit_bt4.text()
                self.PCIPress=self.line_PCI_Press.text()
                BT_angles=[float(self.AngleBT1), float(self.AngleBT2), float(self.AngleBT3), float(self.AngleBT4)]
                # if self.radio_TOS.isChecked(): overtype = "TOS"
                if self.checkBox_overType.isChecked(): overtype = "TOS"
                else:  overtype = "SOT"
                self.B3Dnodes, self.fullnodes, P0_TOP, P0_contactFree, bodyElements_class= \
                    PTN.LayoutAlone3DModelGeneration(savefile[:-4], self.layout.Node, self.layout.Element, self.layout.Elset, \
                        self.layout.Surface, sectors=self.user_sector, offset=BodyOffset,\
                        abaqus=abq, mesh=self.layoutmesh, materialDir=self.materialDir, \
                        btAngles=BT_angles, overtype=overtype, PCIPress=self.PCIPress, \
                            bdw=self.layout.beadWidth*1000, fricView=self.check_FricView.isChecked())
                print ("\n# Layout 3D mesh was saved.")
                self.fullmeshSave=savefile[:-4]
                print (" %s\n"%(savefile))
                line = "Full tire meshes were saved.\n"
                # self.message.setText(line)
                self.check_Direction.setEnabled(True)
                self.Update_ISLM_Material()
                if self.check_FricView.isChecked() == True: 
                    PI = 3.14159265358979323846
                    self.edge_body = bodyElements_class.OuterEdge(self.layout.Node)
                    self.poffset = BodyOffset

                    idxs1 = np.where(self.fullnodes[:,0]<BodyOffset*2)[0]
                    idxs2 = np.where(self.fullnodes[:,0]<BodyOffset)[0]
                    idxs = np.setdiff1d(idxs1, idxs2)
                    self.nd_deleted = self.fullnodes[idxs2]
                    # temp =[]
                    # for ix in idxs2: 
                    #     temp.append([self.fullnodes[ix][0]+BodyOffset, self.fullnodes[ix][0]])
                    self.deletednode = self.fullnodes[idxs]
                    if len(self.layout.RightProfile) > 0: 
                        profiles = []
                        shoCurve = 0 
                        shoLength = 0 
                        for pf in self.layout.RightProfile: 
                            if pf[0]<0: break 
                            if pf[0] ==0: pf[0] = 10.0
                            if shoCurve > 0.0: 
                                shoLength+=pf[1]
                            else:
                                profiles.append(pf)
                            if pf[0] < 0.05: shoCurve = pf[0]

                        if shoCurve > 0.0: 
                            profiles.append([shoCurve, shoLength])

                        pe = [0, 0, 0, self.layout.OD/2]
                        profile=[]
                        Rsho=[]
                        negR = 0 
                        curves =[]
                        for i, pf in enumerate(profiles): 
                            profile.append(pf) 
                            start = pe
                            _, dst, drop = PTN.TD_Arc_length_calculator(profile, h_dist=0, totalwidth=1)
                            end = [0, 0, dst, self.layout.OD/2 - drop] 
                            centers = PTN.Circle_Center_with_2_nodes_radius(pf[0], start, end)
                            if pf[0] < 0: negR = 1
                            if negR == 0:
                                if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
                                else:                                          center = centers[0] 
                            else: 
                                if abs(centers[0][3]) < abs(centers[1][3]):    center = centers[1]
                                else:                                          center = centers[0] 

                            pe = end 
                            curves.append([start, end, center])

                    else: 
                        layoutOuterEdge = self.layout.Element.OuterEdge(self.layout.Node)
                        treadOuterEdge = PTN.GrooveDetectionFromEdge(layoutOuterEdge, self.layout.Node, OnlyTread=0, TreadNumber=0)
                        crown_Edge = PTN.DeleteGrooveEdgeAfterGrooveDetection(treadOuterEdge, self.layout.Node)

                        N = len(crown_Edge.Edge)

                        TWEnd = 0
                        TWStart = 0 
                        CenterEdge = 0 
                        CrownEdge = PTN.EDGE()
                        TopZ = 0.0
                        TopNode = 0
                        LeftMidNode = 0
                        RightMidNode = 0
                        iscentergroove = 0
                        maxY = 0 
                        for i in range(N):
                            N1 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                            N2 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][1])

                            if maxY < N2[2]:  maxY = N2[2]

                            if N1[2] == 0.0:
                                CenterEdge = i
                                CenterNode = N1
                                iscentergroove = 0
                            if N1[2]*N2[2] < 0.0:
                                CenterEdge = i
                                CenterNode = [0, 0.0, 0.0, (N1[3]*abs(N2[2])+N2[3]*abs(N1[2]))/(abs(N1[2])+abs(N2[2]))]
                                iscentergroove = 1

                        if self.layout.TDW <=0.0: self.layout.TDW = maxY * 1.8 
                        # print ("Layout Tread Design width =%.2fmm"%(self.layout.TDW*1000))

                        # print ("No. Center edge", crown_Edge.Edge[CenterEdge]) 
                        
                        if self.layout.shoulderDrop > 0.0: 
                            # hMin = 100.0
                            PreTWNode = []
                            NextTWNode = []
                            TWNode = 0
                            ShoDropRatio = 0
                            for i in range(CenterEdge+1, N):
                                N2 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                                if (self.layout.OD/2000.0 - N2[3] ) <= self.layout.shoulderDrop/1000.0: 
                                    # hMin =  (TireOD/2000.0 - N2[3] ) - Shodrop/1000.0 
                                    PreTWNode=[N2[0], N2[3]]
                                    NextTWNode=[N2[0], N2[3]]
                                    TWNode = N2[0]
                                else:
                                    PreTWNode=[PreTWNode[0], PreTWNode[1], self.layout.OD/2000.0-PreTWNode[1]]
                                    NextTWNode = [N2[0], N2[3], self.layout.OD/2000.0 - N2[3]] 
                                    ShoDropRatio = (self.layout.shoulderDrop/1000-PreTWNode[2]) / (PreTWNode[1] - NextTWNode[1]) 
                                    break
                            
                            
                            TopNode = 0
                            hMax = 0.0
                            for nd in self.layout.Node.Node:
                                if hMax < nd[3] and nd[2] >= 0.0: 
                                    hMax = nd[3]
                                    TopNode = nd[0]
                                    # print ("TOP", nd)

                            Min = 9.9E20;     hMin = 9.9E20
                            Length = 0.0
                            for i in range(CenterEdge, N):
                                if i == CenterEdge:
                                    N2 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                                    Length += sqrt( (CenterNode[2] - N2[2]) * (CenterNode[2] - N2[2]) + (CenterNode[3] - N2[3]) * (CenterNode[3] - N2[3]) )
                                    continue
                                
                                N1 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                                N2 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][1])
                                Length += sqrt( (N1[2] - N2[2]) * (N1[2] - N2[2]) + (N1[3] - N2[3]) * (N1[3] - N2[3]) )
                                # print("right=", Length)
                                if self.layout.TDW /4.0-Length >= 0: 
                                    RightMidNode = N2[0]
                                    # print ("right mid", N2)

                            Min = 9.9E20;     hMin = 9.9E20
                            Length = 0.0
                            for i in range(CenterEdge, -1, -1):
                                if iscentergroove ==1 and i == CenterEdge:
                                    N1 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][1])
                                    Length += sqrt( (CenterNode[2] - N1[2]) * (CenterNode[2] - N1[2]) + (CenterNode[3] - N1[3]) * (CenterNode[3] - N1[3]) )

                                    CenterNode =  self.layout.Node.Node[0]
                                    for nd in  self.layout.Node.Node:
                                        if nd[2] == 0 and nd[3] > CenterNode[3]:   
                                            CenterNode = nd 
                                else:
                                    if i != CenterEdge: 
                                        N1 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                                        N2 =  self.layout.Node.NodeByID(crown_Edge.Edge[i][1])
                                        Length += sqrt( (N1[2] - N2[2]) * (N1[2] - N2[2]) + (N1[3] - N2[3]) * (N1[3] - N2[3]) )
                                # print("Left=", Length)        
                                if self.layout.TDW/4.0-Length >= 0: 
                                    LeftMidNode = N1[0]
                                    # print ("left mid", N1)
                            
                            # N1 =  self.layout.Node.NodeByID(LeftMidNode)
                            # N2 =  self.layout.Node.NodeByID(TopNode)
                            # N3 =  self.layout.Node.NodeByID(RightMidNode)

                            # InitialTR = PTN.CalculateRadiusOf3Points(N1, N2, N3, 23, 3)

                        
                        else: 
                            CriticalAngle = 40.0

                            Min = 9.9E20;     hMin = 9.9E20
                            Length = 0.0
                            for i in range(CenterEdge, N):
                                if i == CenterEdge:
                                    N2 = self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                                    Length += sqrt( (CenterNode[2] - N2[2]) * (CenterNode[2] - N2[2]) + (CenterNode[3] - N2[3]) * (CenterNode[3] - N2[3]) )
                                    # print ("right", NoGrooveCrown.Edge[i], Length*1000, TreadDesignWidth/2.0)
                                    
                                    continue
                                
                                N1 = self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                                N2 = self.layout.Node.NodeByID(crown_Edge.Edge[i][1])
                                Length += sqrt( (N1[2] - N2[2]) * (N1[2] - N2[2]) + (N1[3] - N2[3]) * (N1[3] - N2[3]) )
                                
                                N1a = [N1[0], N1[1], abs(N1[2]), N1[3]]
                                N2a = [N2[0], N2[1], abs(N2[2]), N2[3]]
                                # angle = TIRE.CalculateAngleFrom3Node(N2a, [0, N2a[1], N2a[2]+1.0, N2a[3]], N1a, XY=23)*180.0/PI
                                angle = PTN.Angle_3nodes(N2a, [0, N2a[1], N2a[2]+1.0, N2a[3]], N1a, xy=23)*180.0/PI
                                if self.layout.TDW/2.0-Length >= 0 and abs(angle) < CriticalAngle: 
                                    RightTWNode = N2
                                    # print ("right", NoGrooveCrown.Edge[i], Length*1000, TreadDesignWidth/2.0, angle)
                                if self.layout.TDW/4.0-Length >= 0: RightMidNode = N2

                            # print ("Right TW Node = %d, Right Mid node = %d"%(RightTWNode[0], RightMidNode[0]))
                            # print ("Angle", angle)
                            Min = 9.9E20;     hMin = 9.9E20
                            Length = 0.0
                            for i in range(CenterEdge, -1, -1):
                                if iscentergroove ==1 and i == CenterEdge:
                                    N1 = self.layout.Node.NodeByID(crown_Edge.Edge[i][1])
                                    Length += sqrt( (CenterNode[2] - N1[2]) * (CenterNode[2] - N1[2]) + (CenterNode[3] - N1[3]) * (CenterNode[3] - N1[3]) )
                                    # print ("Left", NoGrooveCrown.Edge[i], Length*1000, TreadDesignWidth/2.0)
                                    CenterNode = self.layout.Node.Node[0]
                                    for nd in self.layout.Node.Node:
                                        if nd[2] == 0 and nd[3] > CenterNode[3]:   
                                            CenterNode = nd 
                                else:
                                    if i != CenterEdge: 
                                        N1 = self.layout.Node.NodeByID(crown_Edge.Edge[i][0])
                                        N2 = self.layout.Node.NodeByID(crown_Edge.Edge[i][1])
                                        Length += sqrt( (N1[2] - N2[2]) * (N1[2] - N2[2]) + (N1[3] - N2[3]) * (N1[3] - N2[3]) )
                                        
                                N1a = [N1[0], N1[1], abs(N1[2]), N1[3]]
                                N2a = [N2[0], N2[1], abs(N2[2]), N2[3]]
                                # angle = TIRE.CalculateAngleFrom3Node(N1a, [0, N1a[1], N1a[2]+1.0, N1a[3]], N2a, XY=23)*180.0/PI
                                angle = PTN.Angle_3nodes(N1a, [0, N1a[1], N1a[2]+1.0, N1a[3]], N2a, xy=23)*180.0/PI
                                if self.layout.TDW/2.0-Length >= 0  and abs(angle) < CriticalAngle: 
                                    LeftTWNode = N1
                                    # print ("Left", NoGrooveCrown.Edge[i], Length*1000, TreadDesignWidth/2.0)
                                if self.layout.TDW/4.0-Length >= 0: LeftMidNode = N1
                            # print ("Left TW Node = %d, Left Mid node = %d"%(LeftTWNode[0], LeftMidNode[0]))
                            # print ("Tread Width = %f"%(TreadDesignWidth))
                            TWStart = LeftTWNode[0];     TWEnd = RightTWNode[0]; 

                            N1 = self.layout.Node.NodeByID(TWStart)
                            N2 = self.layout.Node.NodeByID(TWEnd)
                            # print ("N1", N1, abs(N1[2])-TreadDesignWidth/2000.0)
                            # print ("N2", N2, abs(N2[2])-TreadDesignWidth/2000.0)
                            if abs(N2[2]) > abs(N1[2]):  TWNode = N1[0]
                            else: TWNode = N2[0]

                            cnodes = []
                            for i, ed in enumerate(crown_Edge.Edge): 
                                if i ==0: 
                                    cnodes.append(ed[0])
                                else:
                                    cnodes.append(ed[1])

                            iy = 1000.0
                            for nd in cnodes:
                                nn = self.layout.Node.NodeByID(nd)
                                if iy > abs(nn[2]): 
                                    iy = abs(nn[2])
                                    TopNode = nn[0]
                            # TopNode = CenterNode[0]
                            LeftMidNode = LeftMidNode[0]; RightMidNode = RightMidNode[0]
                            print ("\n\n** Center Node = [%f, %f, %f]"%(CenterNode[1], CenterNode[2], CenterNode[3]))
                            print ("** Sho.Drop Check Node ID : %d, %d -> %d, Crown Center Node ID : %d"%(TWStart, TWEnd, TWNode, TopNode))
                            print ("** Tread Radius check Node ID: %d, %d, Center Node ID : %d"%(LeftMidNode, RightMidNode, TopNode))

                        
                        N1 = self.layout.Node.NodeByID(LeftMidNode)
                        N2 = self.layout.Node.NodeByID(TopNode)
                        N3 = self.layout.Node.NodeByID(RightMidNode)
                        InitialTR = PTN.CalculateRadiusOf3Points(N1, N2, N3, 23, 3)

                        print ("** Tread Radius Assummed=%.1fmm"%(InitialTR*1000))
                        profiles = [[InitialTR, 0.5]]
                        _, dst, drop = PTN.TD_Arc_length_calculator(profiles, h_dist=0, totalwidth=1)
                        start = [0, 0, 0, self.layout.OD/2.0]
                        end = [0, 0, -dst, self.layout.OD/2 - drop]
                        centers = PTN.Circle_Center_with_2_nodes_radius(profiles[0][0], start, end)
                        if centers[0][3] > self.layout.OD/2.0:  center = centers[1]
                        else:  center = centers[0]
                        curves= [[start, end, center]]
                    PTN.FricView_msh_creator(fname=savefile[:-4], 
                        HalfOD=self.layout.OD/2.0, ##
                        body_outer=self.edge_body, ## 
                        body_node=self.B3Dnodes,##   
                        body_offset=BodyOffset,  ## 
                        body_sector=self.user_sector, ##
                        profiles=profiles, ##
                        curves=curves, ## 
                        ptn_top=P0_TOP, ##
                        ptn_free=P0_contactFree, ## 
                        ptn_npn=self.fullnodes, ##
                        ptn_deleted_nodes=self.nd_deleted, ## 
                        ptn_deleted=self.deletednode, ## 
                        ptn_PN=self.user_sector, ## 
                        ptn_PL=float(self.layout.OD*PI / self.user_sector), ## 
                        ptn_offset=BodyOffset, ## 
                        shoulder=self.layout.shoulderType, ## 
                        revPtn=False, grooveTire=1)
            return 

        if self.readlayout == 1 and self.readpattern == 1: 
            if self.treadremoved == 0:     self.removal_tread()
            if self.patternexpanded ==0 :  self.expansion_ptn()
        # if self.readlayout == 0: 
        self.check_Direction.setEnabled(False)

        filename = self.layoutms+"-"+self.ptnms
        savefile, _= QtWidgets.QFileDialog.getSaveFileName(None, "Save files as", self.savedirectory+"/"+filename, "Layout/Pattern Mesh(*.axi *.trd")
        # savefile = self.savedirectory+"/"+filename
        solid_err=[]

        
        POFFSET = 10000
        if self.filesaved == 0: 
            self.pd=0

            hwnd = win32gui.FindWindow(None, self.mainWindowName)
            win32gui.SetForegroundWindow(hwnd)

            print ("\n############################################")
            print ("## Fitting pattern to layout ")
            print ("############################################")
            
            
            if self.layout.shoulderType=="R":
                if  self.layout.r_shocurve < 6.0E-03 or self.shoulderGa >= self.layout.r_shocurve  + 2.0e-03:       self.Check_ShoulderGaugeCheck = 1
                if self.layout.T3DMMODE == 0: 
                    gauge_constant_range=self.layout.TDW/2.0 # + 10.0E-3
                    if self.shoulderGa > self.layout.r_shocurve - 1.0e-03: 
                        gauge_constant_range=self.layout.TDW/2.0 - 10.0E-3
                    # print ("* Groove Depth adjusted after %.2fmm"%(gauge_constant_range*1000))

                    # self.ptn_btm_node_section
                    self.pattern.npn, ptn_elset=PTN.Pattern_Gauge_Adjustment_ToBody(self.flattened_Tread_bottom_sorted, self.pattern.npn, \
                        self.pattern.freebottom, self.pattern.nps, self.layout.OD, gauge_constant_range,\
                        self.pattern.Node_Origin, self.pattern.surf_pattern_pos_side, self.pattern.surf_pattern_neg_side)
                
            self.ptn_gauged = PTN.COPYPTN(self.pattern)  ## important!! Don't move the position.. 

            if self.layout.shoulderType=="R" and self.layout.T3DMMODE== 0: 
                self.pattern.npn =PTN.BendingPattern(OD=self.layout.OD, Rprofiles=self.layout.RightProfile, \
                    Rcurves=self.layout.R_curves, Lprofiles=self.layout.LeftProfile , Lcurves=self.layout.L_curves , nodes=self.pattern.npn,  xy=23)
            else:
                # print (" Profile information before bending ")
                # for pf in self.layout.RightProfile:
                #     print(pf)
                
                self.pattern.npn = PTN.BendingSquarePattern(OD=self.layout.OD, profiles=self.layout.RightProfile, curves=self.layout.R_curves,\
                        nodes=self.pattern.npn, xy=23)

            # self.ptn_bended = PTN.COPYPTN(self.pattern)
            if self.layout.T3DMMODE == 1: 
                self.pattern.npn = PTN.NodesOnSolids(self.pattern.npn, self.pattern.nps)
            self.ptn_bended = PTN.COPYPTN(self.pattern)
            if self.layout.shoulderType=="R"  : 
                self.pattern.npn, self.edge_body, self.pd, pf_ending = PTN.Adjust_PatternBottomSideNodes(self.layout.Node, self.layout.Element, \
                    self.layout.Tread, self.pattern.npn, self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side,\
                    self.pattern.Node_Origin, self.pattern.freebottom, TDW=self.layout.TDW, t3dm=self.layout.T3DMMODE)

            elif self.layout.shoulderType=="S" and self.layout.T3DMMODE == 0:
                self.pattern.npn, self.pattern.sideBtmNode = PTN.AttatchSquarePatternSideNodes(self.layout.sideNodes, self.pattern.npn, self.pattern.Node_Origin, \
                                    self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side)
            self.ptn_bended = PTN.COPYPTN(self.pattern)
            # if self.layout.T3DMMODE ==0 : or self.check_FricView.isChecked() == True : 
            #     self.check_FricView.setDisabled(True)
            if len(self.layout.Tread.Element)  : 
                self.nodes_layout_treadbottom = PTN.Get_layout_treadbottom(self.flattened_Tread_bottom_sorted, np.array(self.InitialLayout.Node.Node))
            if self.layout.shoulderType=="R" : #and self.layout.T3DMMODE ==0: 
                self.pattern.npn = PTN.RepositionNodesAfterShoulder(pf_ending, self.ptn_gauged.npn, self.pattern.surf_pattern_pos_side, self.pattern.surf_pattern_neg_side, \
                        self.pattern.npn,  self.layout.TDW, self.layout.RightProfile, self.layout.R_curves, self.layout.L_curves,\
                        btm_surf=self.pattern.freebottom, ptn_R=self.pattern.diameter/2.0, ptn_TDW=self.pattern.TreadDesignWidth,\
                        bodynodes=self.layout.Node, bodybottom=self.nodes_layout_treadbottom, ptn_orgn=self.pattern.Node_Origin)

            # self.ptn_bended = PTN.COPYPTN(self.pattern)
            if self.layout.shoulderType=="S" and self.layout.T3DMMODE==0: 
                self.pattern.npn = PTN.ShiftShoulderNodesSquarePattern(self.pattern.npn, self.pattern.Node_Origin, self.layout.RightProfile, self.layout.R_curves,\
                        self.layout.sideNodes, self.pattern.surf_pattern_pos_side, self.pattern.surf_pattern_neg_side,\
                        self.pattern.TreadDesignWidth, self.layout.TDW, self.pattern.sideBtmNode )
            start = 0             
            self.pattern.npn = PTN.AttatchBottomNodesToBody(bodynodes=self.layout.Node, \
                bodyelements=self.layout.Element, ptnnodes=self.pattern.npn, \
                    ptnbottom=self.pattern.freebottom, start=start, \
                        shoulder=self.layout.shoulderType, ptnelements=self.pattern.nps)

            if self.layout.shoulderType == 'S' :   self.layout.group ="TBR"
            if self.layout.group =="TBR" : subGa_margin = 0.001 
            elif self.layout.group =="LTR": subGa_margin = 0.0003 
            else: subGa_margin = 0.0003
            self.ptn_elset, self.pattern.nps, self.pattern.npn, self.pattern.surf_pitch_up, self.pattern.surf_pitch_down, \
                 self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side, NewELMatching, NewSurfs\
                 = PTN.PatternElsetDefinition(self.pattern.nps, self.pattern.npn, self.layout.Tread, self.layout.Node,\
                 subtread=self.check_SubTread.isChecked(), btm=1, surf_btm=self.pattern.freebottom, subGaMargin=subGa_margin,\
                 shoulder=self.layout.shoulderType,  tdw=self.layout.TDW, pitchUp=self.pattern.surf_pitch_up, \
                     pitchDown=self.pattern.surf_pitch_down, sideNeg=self.pattern.surf_pattern_neg_side, sidePos=self.pattern.surf_pattern_pos_side, backupSolid=self.ptn_bended)
            if self.check_SubTread.isChecked() and len(self.pattern.SF_fulldepthgroove) and len(NewELMatching):
                NewELMatching = np.array(NewELMatching)

                for nem in NewELMatching: 
                    ix = np.where(self.pattern.Free_Surface_without_BTM[:,0]==nem[0])[0]
                    if len(ix)>0: 
                        for x in ix: 
                            if self.pattern.Free_Surface_without_BTM[x][1] ==2: 
                                self.pattern.Free_Surface_without_BTM[x][0] = nem[1]

                    ix = np.where(self.pattern.SF_fulldepthgroove[:,0]==nem[0])[0]
                    if len(ix)>0: 
                        for x in ix: 
                            if self.pattern.SF_fulldepthgroove[x][1] ==2: 
                                self.pattern.SF_fulldepthgroove[x][0] = nem[1]

                    ix = np.where(self.pattern.PTN_AllFreeSurface[:,0]==nem[0])[0]
                    if len(ix)>0: 
                        for x in ix: 
                            if self.pattern.PTN_AllFreeSurface[x][1] ==2: 
                                self.pattern.PTN_AllFreeSurface[x][0] = nem[1]
                                # print("GRV", self.pattern.PTN_AllFreeSurface[x][0], "Face", self.pattern.PTN_AllFreeSurface[x][1])

                self.pattern.PTN_AllFreeSurface = np.concatenate((self.pattern.PTN_AllFreeSurface, NewSurfs), axis=0)   
            ###################################################################
            ## pattern direction change 
            ###################################################################
            if self.check_Direction.isChecked() :  self.PTN_Direction_Change()
            ###################################################################


            self.check_SubTread.setDisabled(True)
            self.radio_expanded.setChecked(True)
            
            self.ptn_bottomed = PTN.COPYPTN(self.pattern)

            self.pattern.npn = PTN.BendintPatternInCircumferentialDirection(self.pattern.npn, self.layout.OD)
            
            NN = len(self.pattern.npn); NS= len(self.pattern.nps)
            solid_err, text, _, _=PTN.Jacobian_check(self.pattern.npn, self.pattern.nps)  ## deformed pattern mesh check 
             
            if len(solid_err) > 0 : 
                soler = np.array(solid_err)
                soler = soler[:,0]
                btmel = self.pattern.freebottom[:,0]
                btmer = np.intersect1d(btmel, soler)
                txt = "### Elements distorted\n"
                for sd in solid_err: 
                    txt += " %d, "%(sd[0])
                txt += "\n>Trying to relocate the nodes on the bottom solids"
                print (txt)
                if len(btmer) == 0 : 
                    ## Checking the elements of Jacobian < 0.01 
                    ## 만약 구성하는 절점이 pattern의 free surface에 있지 않다면 top 절점의 수직 아래로 강제 이동 시켜 일부 요소 수정 가능 
                    
                    free_surface_nodes= self.ptn_model.Free_Surface_without_BTM[:,7:]

                    free_surface_nodes = np.unique(free_surface_nodes)

                    unchecked = []
                    checked = []
                    for sl in solid_err: 
                        
                        ernodes = []
                        ernodes.append(sl[1]); ernodes.append(sl[2]); ernodes.append(sl[3]); ernodes.append(sl[4]); 
                        ernodes.append(sl[5]); ernodes.append(sl[6])
                        if sl[7] > 0: 
                            ernodes.append(sl[7]); ernodes.append(sl[8])

                        ernodes = np.array(ernodes)
                        ern = np.setdiff1d(ernodes, free_surface_nodes)
                        tmp=[sl[0], sl[1], sl[2], sl[3], sl[4], sl[5], sl[6], sl[7], sl[8], len(ern), ern]
                        checked.append(tmp)
                    checked = sorted(checked, key = lambda val : val[9])
                    for sl in checked: 
                        if sl[9] > 0 : 
                            for nd in sl[10]: 
                                ix1=0; ix2 = 0 
                                if nd == sl[1] : 
                                    ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                    if sl[7] > 0: 
                                        ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                                    else: 
                                        ix2 = np.where(self.pattern.npn[:,0]==sl[4])[0][0]
                                    self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                    self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 
                                    # print ("   N1 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)

                                elif nd == sl[2]: 
                                    ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                    if sl[7] > 0: 
                                        ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                                    else: 
                                        ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                                    self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                    self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2]
                                    # print ("   N2 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)

                                elif nd == sl[3]: 
                                    ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                    if sl[7] > 0: 
                                        ix2 = np.where(self.pattern.npn[:,0]==sl[7])[0][0]
                                    else: 
                                        ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                                    # print ("   N3 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)
                                    # print ("    %6.2f, %6.2f,     %6.2f,%6.2f"%( self.pattern.npn[ix1][1]*1000, self.pattern.npn[ix1][2]*1000, self.pattern.npn[ix2][1]*1000, self.pattern.npn[ix2][2]*1000))
                                    self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                    self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 
                                    # print (" >> %6.2f, %6.2f "%(self.pattern.npn[ix1][1]*1000, self.pattern.npn[ix1][2]*1000))

                                elif nd == sl[4] and sl[7] > 0: 
                                    ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                    if sl[7] > 0: 
                                        ix2 = np.where(self.pattern.npn[:,0]==sl[8])[0][0]
                                    self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                    self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 
                                    # print ("   N4 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)
                        else:
                            unchecked.append(sl)
                    
                    for sl in unchecked:     
                        ix1 = np.where(self.pattern.npn[:,0]==sl[1])[0][0]
                        if sl[7] > 0: 
                            ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                        else: 
                            ix2 = np.where(self.pattern.npn[:,0]==sl[4])[0][0]
                        self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                        self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                        ix1 = np.where(self.pattern.npn[:,0]==sl[2])[0][0]
                        if sl[7] > 0: 
                            ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                        else: 
                            ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                        self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                        self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                        ix1 = np.where(self.pattern.npn[:,0]==sl[3])[0][0]
                        if sl[7] > 0: 
                            ix2 = np.where(self.pattern.npn[:,0]==sl[7])[0][0]
                        else: 
                            ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                        self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                        self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                        if sl[7] > 0: 
                            ix1 = np.where(self.pattern.npn[:,0]==sl[4])[0][0]
                            ix2 = np.where(self.pattern.npn[:,0]==sl[8])[0][0]
                            self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                            self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                    solid_err, text, negative_ht, sm_lth=PTN.Jacobian_check(self.pattern.npn, self.pattern.nps)  ## deformed pattern mesh check 

            if len(solid_err) > 0 : 
                print (text)
                print ("#############################################")
                print ("### %d elements in Pattern mesh is distorted"%(len(solid_err)))
                print ("#############################################\n")
                # PTN.WritePatternPitch(self.pattern.npn, self.pattern.nps, file=self.cwd+"0-Distorted-"+self.layoutms+"-"+self.ptnms +".inp", body_node=self.layout.Node, body_element=self.layout.Element)

                txt = "### Elements distorted\n"
                for sd in solid_err: 
                    txt += " %d, "%(sd[0])
                print (txt)
            
            self.btn_generation.setEnabled(True)
            
            # self.input_layout_sector.setDisabled(True)
            self.figure.plot(layout=self.layout, pattern=self.pattern, show='all', ptn_elset=self.ptn_elset, bended=1)
            self.ShowingImage = 'layout'
            
            if len(solid_err) > 0 :
                return 

            NN = len(self.pattern.npn); NS= len(self.pattern.nps)
            NN = int(np.max(self.pattern.npn[:,0])) - 10**7
            NS = int(np.max(self.pattern.nps[:,0])) - 10**7 
            if NN > NS: POFFSET=int(NN/10000) * 10000 + 10000
            else:       POFFSET=int(NS/10000) * 10000 + 10000
            self.poffset = POFFSET
            print ("* ID Max. Node=%d, Element=%d"%(NN, NS))

            # if   self.layout.shoulderType=="S" and self.layout.T3DMMODE ==0 : return 
             
            self.nd_deleted=[]
            self.fullnodes=[]
            self.fullsolids=[]

            pitch_side = [self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side]
            self.fullnodes, self.fullsolids, self.elset3d, self.surf_XTRD1001, self.surf_YTIE1001, self.nd_deleted, self.deletednode, \
            XTRD_surface, YTIE_surface= PTN.GenerateFullPatternMesh(self.pattern.npn, self.pattern.nps, self.pattern.NoPitch, self.layout.OD, self.pattern.surf_pitch_up, self.pattern.surf_pitch_down, \
                surf_free=self.pattern.PTN_AllFreeSurface, surf_btm=self.pattern.freebottom, surf_side=pitch_side, elset=self.ptn_elset, \
                offset=POFFSET, pl=self.pattern.TargetPL, ptn_org=self.pattern.Node_Origin, ptn_pl=self.pattern.pitchlength, pd=self.pd , \
                    rev=self.check_Direction.isChecked(), shoulderType=self.layout.shoulderType)
            

        if self.filesaved == 0 and len(solid_err) == 0: 
            self.btn_removetread.setDisabled(True)
            self.btn_expansion.setDisabled(True)
            self.filesaved = 1 


        if savefile and len(solid_err) == 0:
            self.user_sector=int(self.input_layout_sector.text()) 
            BodySector = self.user_sector

            print ("\n** Full 3D Mesh ")
            print ("** Pattern Start =%d, Offset=%d\n** Layout Start=%d, Offset=%d\n** No. of body sectors=%d\n"%(self.Pattern_start_number, self.poffset, BodyStartNo, BodyOffset, BodySector))
            if self.layout.T3DMMODE ==1 or self.layout.shoulderType == "S":   
                self.edge_body = self.layout.Element.OuterEdge(self.layout.Node)
            self.B3Dnodes, self.B3Del4, self.B3Del6, self.B3Del8, self.B3Delset, self.B3Dsurface, self.Bodysurf = \
            PTN.GenerateFullBodyMesh(self.layout.body_nodes, self.layout.Element, self.layout.Elset, \
                surfaces=self.layout.Surface, body_outer=self.edge_body, sectors=BodySector, offset=BodyOffset)
            


            savefile = savefile[:-4]
            isCtb=0
            isSut=0 
            for eset in self.layout.Elset.Elset: 
                if eset[0] == "CTR" or eset[0] == 'CTB': isCtb = 1
                if eset[0] == "UTR" or eset[0] == 'SUT': isSut = 1
            namechange = [isCtb, isSut]

            if self.ABAQUS.isChecked() == True:  
                abq = 1
                namechange = [0, 0] 
            else: abq = 0 
            # print (" Pattern off", POFFSET)
            PTN.Write_SMART_PatternMesh(file=savefile +".trd", nodes=self.fullnodes, elements=self.fullsolids , elsets=self.elset3d, XTRD=self.surf_XTRD1001, \
                YTIE=self.surf_YTIE1001, ties=[], start=self.Pattern_start_number, offset=self.poffset, namechange=namechange, abaqus=abq, revPtn=self.check_Direction.isChecked())#self.poffset)
            PTN.Write_SMART_TireBodyMesh(file=savefile  + ".axi", nodes=self.B3Dnodes, el4=self.B3Del4, el6=self.B3Del6, el8=self.B3Del8, elsets=self.B3Delset, surfaces=self.B3Dsurface,\
                surf_body=self.Bodysurf, ties=self.layout.Tie, txtelset=self.layout.TxtElset, start=BodyStartNo, offset=BodyOffset, abaqus=abq)

            # PTN.SolidComponents_checking(fname=savefile+"_solids.dat", trd=savefile +".trd", axi=savefile +".axi")
            self.AngleBT1=self.lineEdit_bt1.text()
            self.AngleBT2=self.lineEdit_bt2.text()
            self.AngleBT3=self.lineEdit_bt3.text()
            self.AngleBT4=self.lineEdit_bt4.text()
            self.PCIPress=self.line_PCI_Press.text()
            BT_angles=[float(self.AngleBT1), float(self.AngleBT2), float(self.AngleBT3), float(self.AngleBT4)]
            if self.checkBox_overType.isChecked(): overtype = "TOS"
            else:  overtype = "SOT"
            PTN.SmartMaterialInput(axi=savefile +".axi", trd=savefile +".trd", layout=self.layoutmesh, \
                elset=self.layout.Elset.Elset, node=self.layout.Node.Node, element=self.layout.Element.Element,\
                     materialDir=self.materialDir, btAngles=BT_angles, overtype=overtype, PCIPress=self.PCIPress, bdw=self.layout.beadWidth*1000, pattern=self.readpattern)
            line = "Full tire meshes were saved.\n"
            self.fullmeshSave=savefile 
            self.Update_ISLM_Material()
            # self.message.setText(line)

             ## writing pattern single pitch   #XTRD_surface, YTIE_surface
            filename = savefile+"-P3DM.ptn"
            # try: 
            P0_TOP, P0_SelfContact = PTN.Creating_pattern_pitch(self.ptn_bottomed, self.pattern, self.layout.LeftProfile, self.layout.RightProfile, \
                self.layout.L_curves, self.layout.R_curves, self.layout.OD, self.layout.GD, TDW=self.layout.TDW, \
                fname=filename, PN=self.pattern.NoPitch, pitch_up=self.pattern.surf_pitch_up, pitch_down=self.pattern.surf_pitch_down, \
                pitch_side_pos=self.pattern.surf_pattern_pos_side, pitch_side_neg=self.pattern.surf_pattern_neg_side, \
                bottom_surf=self.pattern.freebottom, top_free=self.pattern.freetop, xtrd=XTRD_surface, ytie=YTIE_surface, revPtn=self.check_Direction.isChecked())
            # print ("\n## Single Pitch Mesh is created.")
            # print ("  %s"%(filename.split("/")[-1]))
            # except:
            #     print ("\n Single pitch mesh was not created.")
            filename = savefile+"-L2DM.inp"
            if len(self.layout.Tread.Element) > 0: 
                PTN.Creating_tread_removed_layout(fname=filename, nodes=self.layout.body_nodes, elements=self.layout.Element, elsets=self.layout.Elset,\
                surfaces=self.layout.Surface, ties=self.layout.Tie, treads=self.layout.Tread, all_nodes=self.layout.Node)
                print ("## Tread Removed Mesh is created.")
                print ("  %s\n"%(filename.split("/")[-1]))

            # self.nd_deleted=[]; self.fullnodes=[], P0_TOP, P0_SelfContact  ## 
            # P0_TOP = np.concatenate((P0_TOP), axis=0)
            if self.check_FricView.isChecked() == True:
                # if len(self.ptn_model.SF_fulldepthgroove) > 0: 
                #     counting = 0 
                #     for surf in self.ptn_model.SF_fulldepthgroove: 
                #         print (surf[0], ", ", surf[1], ", ", surf[7], ", ", surf[8], ", ", surf[9], ", ", surf[10])
                #         ix1 = np.where(P0_SelfContact[:,0]==surf[0])[0]
                #         ix2 = np.where(P0_SelfContact[:,1]==surf[1] )[0]
                #         ix = np.intersect1d(ix1, ix2)
                #         if len(ix) ==0:
                #             P0_SelfContact = np.append(P0_SelfContact, surf, axis=0)
                #             counting+=1
                #     print ("** Grv Btm(%d) is added to free surface"%(counting))

                P0_contactFree = np.concatenate((self.pattern.freebottom, self.pattern.surf_pattern_pos_side, self.pattern.surf_pattern_neg_side, P0_SelfContact ), axis=0)
                idx = np.where(P0_contactFree[:,0]==10**7+3450)[0]
                PTN.FricView_msh_creator(fname=savefile, HalfOD=self.layout.OD/2.0, body_outer=self.edge_body,body_node=self.B3Dnodes,\
                            body_offset=BodyOffset, body_sector=self.user_sector, profiles=self.layout.RightProfile, curves=self.layout.R_curves,\
                            ptn_top=P0_TOP, ptn_free=P0_contactFree, ptn_npn=self.fullnodes, ptn_deleted_nodes=self.nd_deleted, \
                            ptn_deleted=self.deletednode, ptn_PN=self.pattern.NoPitch, ptn_PL=self.pattern.TargetPL, ptn_offset=self.poffset,\
                            shoulder=self.layout.shoulderType, revPtn=self.check_Direction.isChecked())

            

    def showLayoutNo(self): 
    
        if self.checkBox_No.isChecked(): 
            self.LayoutNo = 1 
        else: 
            self.LayoutNo = 0 
        
        if self.radio_layout.isChecked(): 
            self.showlayout()
        elif self.radio_untreaded.isChecked(): 
            self.showuntreaded()

    def UncheckOverlayRadio(self): 
        self.radio_Maingrv.setChecked(False)
        self.radio_Subgrv.setChecked(False)
        self.radio_Kerf.setChecked(False)
        self.radio_AllSide.setChecked(False)
    
    ## layout based plot ##########################
    def showcurrentlayout(self): 
        self.UncheckOverlayRadio()
        try:
            if self.radio_model.isChecked() : 
                ptn = self.ptn_model
                bending = 0
            elif self.radio_scaled.isChecked() : 
                ptn = self.ptn_expanded
                bending = 0 
            elif self.radio_gauged.isChecked() : 
                ptn = self.ptn_gauged
                bending = 0 
            elif self.radio_bended.isChecked() : 
                ptn = self.ptn_bended
                bending =0 
            else : 
                ptn = self.pattern
                bending = 1 
                
            # self.message.setText("Layout has been plotted.")
            self.figure.plot(layout=self.layout, pattern=ptn, show='all', ptn_elset=self.ptn_elset, bended=bending)
            self.ShowingImage = 'layout'
            

        except:
            try: 
                self.figure.plot(layout=self.InitialLayout, show='layout')
                self.ShowingImage = 'layout'
            except:
                # self.message.setText("Layout has not been plotted.")
                self.figure.plot(show='none')
                self.ShowingImage = 'none'
    def showlayout(self): 
        self.UncheckOverlayRadio()
        try:      
            # print ("initial el no=%d"%(len(self.InitialLayout.Element.Element)))
            # self.message.setText("Initial layout has been plotted.")
            self.figure.plot(layout=self.InitialLayout, show='layout', layoutNo=self.LayoutNo)
            self.ShowingImage = 'layout'
        except:
            # self.message.setText("Initial layout has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showuntreaded(self): 
        self.UncheckOverlayRadio()

        try:
            # print ("initial el no=%d, removed=%d"%(len(self.InitialLayout.Element.Element), len(self.UntreadedLayout.Element.Element)))
            # self.message.setText("Layout without tread has been plotted")
            self.figure.plot(layout=self.UntreadedLayout, show='layout', layoutNo=self.LayoutNo, flattened_tread = self.flattened_Tread_bottom_sorted)
            self.ShowingImage = 'layout'

        except:
            # self.message.setText("Layout without tread has not been plotted")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showsolid(self): 
        self.UncheckOverlayRadio()
        points=[[1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1]]
        if self.readpattern and self.ShowingImage != 'layout': 
            solid = self.SearchedSolids(id=0)
            try: 
                if self.radio_model.isChecked() : 
                    npn = self.ptn_model.npn 
                elif self.radio_scaled.isChecked() : 
                    npn = self.ptn_expanded.npn 
                elif self.radio_gauged.isChecked() : 
                    npn = self.ptn_gauged.npn 
                elif self.radio_bended.isChecked() : 
                    npn = self.ptn_bended.npn 
                elif self.radio_expanded.isChecked() : 
                    npn = self.ptn_bottomed.npn 
                else : 
                    npn = self.pattern.npn 
                if len(solid) > 0:  print ("\n Pattern Element" )
                for sd in solid: 
                    ix=np.where(npn[:,0]==sd[1])[0][0]; n1=npn[ix]
                    ix=np.where(npn[:,0]==sd[2])[0][0]; n2=npn[ix]
                    ix=np.where(npn[:,0]==sd[3])[0][0]; n3=npn[ix]
                    ix=np.where(npn[:,0]==sd[4])[0][0]; n4=npn[ix]
                    ix=np.where(npn[:,0]==sd[5])[0][0]; n5=npn[ix]
                    ix=np.where(npn[:,0]==sd[6])[0][0]; n6=npn[ix]
                    if sd[7] > 0: 
                        ix=np.where(npn[:,0]==sd[7])[0][0]; n7=npn[ix]
                        ix=np.where(npn[:,0]==sd[8])[0][0]; n8=npn[ix]
                        Js =[]
                        for pt in points: 
                            Js.append( PTN.Jacobian_Hexahedron(n1, n2, n3, n4, n5, n6, n7, n8, r=pt[0], s=pt[1], t=pt[2]))
                            # print("%e"%(PTN.Jacobian_Hexahedron(n1, n2, n3, n4, n5, n6, n7, n8, r=pt[0], s=pt[1], t=pt[2])))
                        print ("%4d(%4d,%4d,%4d,%4d,%4d,%4d,%4d,%4d, J=%.1E)"%(sd[0]-10**7, sd[1]-10**7,\
                             sd[2]-10**7, sd[3]-10**7, sd[4]-10**7, sd[5]-10**7, sd[6]-10**7, sd[7]-10**7, sd[8]-10**7 , min(Js)*10**9))
                    else: 
                        Js =[]
                        for m, pt in enumerate(points):
                            if m ==0 or m ==1 or m ==4 or m==5: continue 
                            # if m ==0: pt =[0, 0, -1]
                            # if m == 4: pt = [1, 0, 1]
                            # if m == 1: pt = [0, 0, -1]
                            # if m == 5: pt = [1, 0, 1]
                            Js.append( PTN.Jacobian_Hexahedron(n1, n1, n2, n3, n4, n4, n5, n6, r=pt[0], s=pt[1], t=pt[2]) )
                            # print("%e"%(PTN.Jacobian_Hexahedron(n1, n1, n2, n3, n4, n4, n5, n6, r=pt[0], s=pt[1], t=pt[2])))
                        print ("%4d(%4d,%4d,%4d,%4d,%4d,%4d, J=%.1E)"%(sd[0]-10**7, sd[1]-10**7,\
                             sd[2]-10**7, sd[3]-10**7, sd[4]-10**7, sd[5]-10**7, sd[6]-10**7, min(Js)*10**9))

                self.figure.plot_error(solid, npn) 
                self.ShowingImage = '3D'
            except: 
                print("Solid element cannot be plotted.")

        elif self.readlayout: 
            npp = []
            for el in self.InitialLayout.Element.Element: 
                npp.append([el[0], el[1], el[2], el[3],el[4], el[6]] )
            npp = np.array(npp)
            npn = []
            plane, solid = self.SearchElements(npp, id=0) 
            if len(plane) > 0: 
                print ("\n Layout Element")
                for pn in plane: 
                    if pn[6] == 2: print (" %5d, %5d, %5d"%(pn[0], pn[1], pn[2]))
                    if pn[6] == 3: print (" %5d, %5d, %5d, %5d"%(pn[0], pn[1], pn[2], pn[3]))
                    if pn[6] == 4: print (" %5d, %5d, %5d, %5d, %5d"%(pn[0], pn[1], pn[2], pn[3], pn[4]))
            if len(solid) > 0: 
                

                print ("\n Pattern Element" )
                for sd in solid: 
                    if sd[7] > 0: 
                        print ("%5d,%5d,%5d,%5d,%5d,%5d,%5d,%5d,%5d"%(sd[0]-10**7, sd[1]-10**7, sd[2]-10**7, sd[3]-10**7, sd[4]-10**7, sd[5]-10**7, sd[6]-10**7, sd[7]-10**7, sd[8]-10**7 ))
                    else: 
                        print ("%5d,%5d,%5d,%5d,%5d,%5d,%5d"%(sd[0]-10**7, sd[1]-10**7, sd[2]-10**7, sd[3]-10**7, sd[4]-10**7, sd[5]-10**7, sd[6]-10**7))
            if self.radio_model.isChecked() : 
                npn = self.ptn_model.npn 
            elif self.radio_scaled.isChecked() : 
                npn = self.ptn_expanded.npn 
            elif self.radio_gauged.isChecked() : 
                npn = self.ptn_gauged.npn 
            elif self.radio_bended.isChecked() : 
                npn = self.ptn_bended.npn 
            elif self.radio_expanded.isChecked() : 
                npn = self.ptn_bottomed.npn 
            else : 
                npn = self.pattern.npn

            self.figure.Add_layer(plane, np.array(self.InitialLayout.Node.Node), solid, npn)

    def SearchElements(self, npp, id=1): 
                  
        solid = []
        plane = []
        if self.readlayout:
            solidel = self.searchno.text()
            if self.radio_model.isChecked() : 
                solids = self.ptn_model.nps 
            elif self.radio_scaled.isChecked() : 
                solids = self.ptn_expanded.nps 
            elif self.radio_gauged.isChecked() : 
                solids = self.ptn_gauged.nps 
            elif self.radio_bended.isChecked() : 
                solids = self.ptn_bended.nps 
            elif self.radio_expanded.isChecked() : 
                solids = self.ptn_bottomed.nps 
            else : 
                solids = self.pattern.nps 

            if solidel != "" and solidel != "0": 
                if "," in solidel: 
                    els = solidel.split(",")
                else: 
                    els = [solidel.strip()]
                
                tns=[]
                    
                try: 
                    for el in els: 
                        el = el.strip()
                        
                        if "*" in el[0]: 
                            el = el[1:]
                            if "+" in el: 
                                el = el.split("+") 
                                el = int(el[0].strip())   
                                if el< 10**7:   el += 10**7     
                                el = str(int(el))+"+"     
                            elif "~" in el: 
                                ns = el.split("~")
                                ns[0] = int(ns[0].strip())
                                ns[1] = int(ns[1].strip())
                                if ns[0] < 10**7: ns[0] += 10**7 
                                ns[0] = str(ns[0])
                                if ns[1] < 10**7: ns[1] += 10**7 
                                ns[1] = str(ns[1])
                                el = ns[0] +"~" + ns[1]
                            else: 
                                el = int(el.strip()) 
                                if el < 10**7: el += 10**7 
                                el = str(int(el))

                        if "+" in el:
                            el = el.split("+") 
                            el = int(el[0].strip())

                            if el >= 10**7 and self.readpattern:
                                ix = np.where(solids[:,0] == el)[0]
                                if len(ix) == 1: 
                                    el = solids[ix[0]]
                                    if el[7] > 0: 
                                        ns = [el[1], el[2], el[3], el[4], el[5], el[6], el[7], el[8]]
                                    else: 
                                        ns = [el[1], el[2], el[3], el[4], el[5], el[6]]
                                    for n in ns: 
                                        ix = np.where(solids.nps[:,1:9] == n)[0]
                                        tns = np.append(tns, ix)#, axis=None)
                                    for tn in tns: 
                                        if id==1 : solid.append(solids[int(tn)][0])
                                        else:  solid.append(solids[int(tn)])
                            else: 
                                # npn = np.array(layout.Node.Node)
                                # elem = layout.Element.Element 
                                nds = []
                                idx = np.where(npp[:,0]== el)[0]
                                if len(idx) == 1: 
                                    idx = idx[0]
                                    element = npp[idx]
                                    nds.append(element[1]); nds.append(element[2])
                                    if element[3] > 0: nds.append(element[3])
                                    if element[4] > 0: nds.append(element[4])
                                    elix = []
                                    for nd in nds: 
                                        idx = np.where(npp[:,1:5]== nd)[0]
                                        if len(idx) > 0: 
                                            for ix in idx: 
                                                elix.append(ix)
                                    elix = np.array(elix)
                                    elix = np.unique(elix)

                                    for elx in elix: 
                                        if id == 1: plane.append(self.InitialLayout.Element.Element[elx][0])
                                        else: plane.append(self.InitialLayout.Element.Element[elx])

                        elif "~" in el:
                            ns = el.split("~")

                            ns[0] = int(ns[0].strip())
                            ns[1] = int(ns[1].strip())
                            if ns[0] >= 10**7 and ns[1] >= 10**7  and self.readpattern: 
                                for i in range(ns[0], ns[1]+1): 
                                    ix = np.where(solids[:,0]==i)[0]
                                    if len(ix) ==1:    
                                        if id== 0: solid.append(solids[ix[0]])
                                        else: solid.append(solids[ix[0]][0])
                            else: 
                                for i in range(ns[0], ns[1]+1): 
                                    ix = np.where(npp[:,0]==i)[0]
                                    if len(ix) ==1:    
                                        if id == 1: plane.append(self.InitialLayout.Element.Element[ix[0]][0])
                                        else: plane.append(self.InitialLayout.Element.Element[ix[0]])


                        elif "" != el and "0" != el: 
                            el = int(el.strip())
                            if el >= 10**7  and self.readpattern: 
                                ix = np.where(solids[:,0]==el)[0]
                                if len(ix) ==1:  
                                    if id==0: solid.append(solids[ix[0]])
                                    else: solid.append(solids[ix[0]][0])
                            else: 
                                ix = np.where(npp[:,0]==el)[0]
                                if len(ix) ==1:    
                                    ix = ix[0]
                                    if id == 1: plane.append(self.InitialLayout.Element.Element[ix][0])
                                    else: plane.append(self.InitialLayout.Element.Element[ix])
                        
                    return plane, solid 
                except:
                    print ("# Error to identify the number of elements")
                    print ("# Possible expressions (*:pattern)")
                    print ("  252, 333~336, *232, *12~20, 236+, *236+")
                    return plane, solid 
            else: 
                # print ("*%s*"%(solidel))
                return plane, solid 
    def SearchedSolids(self, id=1): 
        try:
            if self.readpattern:
                solidel = self.searchno.text()

                if self.radio_model.isChecked() :  solids = self.ptn_model.nps
                elif self.radio_scaled.isChecked() :  solids = self.ptn_expanded.nps
                elif self.radio_gauged.isChecked() :  solids = self.ptn_gauged.nps
                elif self.radio_bended.isChecked() :  solids = self.ptn_bended.nps
                else:                              
                    solids = self.ptn_bottomed.nps
                    # print ("show bottommed elements", solidel)
                
                if solidel != "" and solidel != "0": 
                    if "," in solidel: 
                        els = solidel.split(",")
                    else: 
                        els = [solidel]
                    
                    tns=[]
                    solid = []
                    try: 
                        for el in els: 
                            el = el.strip()
                            if "*" in el[0]: 
                                el = el[1:]
                                if "+" in el: 
                                    el = el.split("+") 
                                    el = int(el[0].strip())    
                                    if el< 10**7:   el += 10**7     
                                    el = str(int(el))+"+"   
                                elif "~" in el: 
                                    pass    
                                else: 
                                    el = int(el.strip()) 
                                    if el< 10**7:   el += 10**7 
                                    el = str(int(el))

                            if "+" in el:
                                # print(el) 
                                el = el.split("+") 
                                el = int(el[0].strip())
                                
                                if el < 10**7: el += 10**7 
                                ix = np.where(solids[:,0] == el)[0]
                                if len(ix) == 1: 
                                    el = solids[ix[0]]
                                    # solid.append(el)
                                    # print (el)
                                    if el[7] > 0: 
                                        ns = [el[1], el[2], el[3], el[4], el[5], el[6], el[7], el[8]]
                                    else: 
                                        ns = [el[1], el[2], el[3], el[4], el[5], el[6]]
                                    for n in ns: 
                                        ix = np.where(solids[:,1:9] == n)[0]
                                        tns = np.append(tns, ix)#, axis=None)
                                    tns = np.unique(tns)
                                    # print (tns)
                                    for tn in tns: 
                                        # print (int(tn),", ", solids[int(tn)][0])
                                        if id==1 : solid.append(solids[int(tn)][0])
                                        else:  solid.append(solids[int(tn)])
                                        # print (solids[tn][0])

                            elif "~" in el:
                                # print(el) 
                                ns = el.split("~")
                                ns[0] = int(ns[0].strip())
                                ns[1] = int(ns[1].strip())
                                if ns[0] < 10**7: ns[0] += 10**7 
                                if ns[1] < 10**7: ns[1] += 10**7 
                                for i in range(ns[0], ns[1]+1): 
                                    ix = np.where(solids[:,0]==i)[0]
                                    if len(ix) ==1:    
                                        if id== 0: solid.append(solids[ix[0]])
                                        else: solid.append(solids[ix[0]][0])
                                        # print (solids[ix[0]][0])


                            elif "" != el and "0" != el: 
                                # print(el)
                                el = int(el.strip())
                                if el < 10**7: el += 10**7
                                ix = np.where(solids[:,0]==el)[0]
                                if len(ix) ==1:  
                                    if id==0: solid.append(solids[ix[0]])
                                    else: solid.append(solids[ix[0]][0])
                                    # print (solids[ix[0]][0])
                            
                        return solid 
                    except:
                        print ("# Error to identify the number of elements")
                        print ("# Possible expressions (*:pattern)")
                        print ("  252, 333~336, *232, *12~20, 236+, *236+")
                        solid=[]
                        return solid 

                else: 
                    # print ("*%s*"%(solidel))
                    solidid = []
                    return solidid
        except:
            pass 

    ## pattern plot ##################################
    def showDefault(self):  ## Pattern Default 
        self.UncheckOverlayRadio()      
        self.searchsolid = self.SearchedSolids(id=1) 
        try:
            if self.radio_model.isChecked() : 
                self.figure.plot(pattern=self.ptn_model, show='pattern', search=self.searchsolid)
            elif self.radio_scaled.isChecked() : 
                self.figure.plot(pattern=self.ptn_expanded, show='pattern', search=self.searchsolid)
            elif self.radio_gauged.isChecked() : 
                self.figure.plot(pattern=self.ptn_gauged, show='pattern', search=self.searchsolid)
            elif self.radio_bended.isChecked() : 
                self.figure.plot(pattern=self.ptn_bended, show='pattern', search=self.searchsolid)
            else : 
                self.figure.plot(pattern=self.ptn_bottomed, show='pattern', search=self.searchsolid)
            self.ShowingImage = 'pattern'
        except:
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showTopSurface(self):   ## Pattern Top Surface
        self.UncheckOverlayRadio()      
        self.searchsolid = self.SearchedSolids(id=1)
        if self.checkBox_SurfNo.isChecked():  number = 1
        else: number = 0 
        try:
            if self.radio_model.isChecked() : 
                surface2plot = self.ptn_model.freetop 
                node2plot = self.ptn_model.npn
            elif self.radio_scaled.isChecked() : 
                surface2plot = self.ptn_expanded.freetop 
                node2plot = self.ptn_expanded.npn
            elif self.radio_gauged.isChecked() : 
                surface2plot = self.ptn_gauged.freetop 
                node2plot = self.ptn_gauged.npn
            elif self.radio_bended.isChecked() : 
                surface2plot = self.ptn_bended.freetop 
                node2plot = self.ptn_bended.npn
            else : 
                surface2plot = self.ptn_bottomed.freetop 
                node2plot = self.ptn_bottomed.npn 
            self.figure.plot_surface(surface2plot, node2plot, search=self.searchsolid, number=number)
            # self.message.setText("Pattern Top Surface has been plotted.")
            self.ShowingImage = 'pattern'
        except:
            # self.message.setText("Pattern Top Surface has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showBottomSurface(self):     ## Pattern Bottom Surface
        self.UncheckOverlayRadio()      
        self.searchsolid = self.SearchedSolids(id=1)
        if self.checkBox_SurfNo.isChecked():  number = 1
        else: number = 0 
        try:
            if self.radio_model.isChecked() : 
                surface2plot = self.ptn_model.freebottom 
                node2plot = self.ptn_model.npn
            elif self.radio_scaled.isChecked() : 
                surface2plot = self.ptn_expanded.freebottom 
                node2plot = self.ptn_expanded.npn
            elif self.radio_gauged.isChecked() : 
                surface2plot = self.ptn_gauged.freebottom 
                node2plot = self.ptn_gauged.npn
            elif self.radio_bended.isChecked() : 
                surface2plot = self.ptn_bended.freebottom 
                node2plot = self.ptn_bended.npn
            else : 
                surface2plot = self.ptn_bottomed.freebottom 
                node2plot = self.ptn_bottomed.npn 
            self.figure.plot_surface(surface2plot,node2plot, search=self.searchsolid, number=number)
            self.ShowingImage = 'pattern'
            # self.message.setText("Pattern Bottom Surface has been plotted.")
        except:
            # self.message.setText("Pattern Bottom Surface has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showPitch(self):      ## Pattern Pitch up Surface
        self.UncheckOverlayRadio()  
        
        self.searchsolid = self.SearchedSolids(id=1) 
        if self.checkBox_SurfNo.isChecked():  number = 1
        else: number = 0 
        try:
            
            if self.radio_model.isChecked() : 
                node2plot = self.ptn_model.npn
                surface2plot = self.ptn_model.surf_pitch_up
                surface2plot1   = self.ptn_model.surf_pitch_down
            elif self.radio_scaled.isChecked() : 
                node2plot = self.ptn_expanded.npn
                surface2plot = self.ptn_expanded.surf_pitch_up
                surface2plot1   = self.ptn_expanded.surf_pitch_down
            elif self.radio_gauged.isChecked() : 
                node2plot = self.ptn_gauged.npn
                surface2plot = self.ptn_gauged.surf_pitch_up
                surface2plot1   = self.ptn_gauged.surf_pitch_down
            elif self.radio_bended.isChecked() : 
                node2plot = self.ptn_bended.npn
                surface2plot = self.ptn_bended.surf_pitch_up
                surface2plot1   = self.ptn_bended.surf_pitch_down
            else : 
                node2plot = self.ptn_bottomed.npn 
                surface2plot = self.ptn_bottomed.surf_pitch_up
                surface2plot1   = self.ptn_bottomed.surf_pitch_down

            if len(surface2plot) > 0: 
                R = np.max(node2plot[:,3])
                Ga = R - np.min(node2plot[:,3])
                down = np.min(node2plot[:,1]) - 5E-03
                up = np.max(node2plot[:,1]) + Ga + 0.001
                self.figure.plot_pitch_surface(surface2plot,surface2plot1, node2plot, search=self.searchsolid, R=R, number=number , downpos=down, uppos=up)
                # self.message.setText("Pattern Pitch up Surface has been plotted.")
                self.ShowingImage = 'pattern'
            else: 
                print ("No Pitch UP surface")
        except:
            # self.message.setText("Pattern Pitch up Surface has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showSide(self):      ## Pattern Side Surface 
        self.UncheckOverlayRadio()  
        self.searchsolid = self.SearchedSolids(id=1) 
        if self.checkBox_SurfNo.isChecked():  number = 3
        else: number = 0 
        try:
            
            if self.radio_model.isChecked() : 
                node2plot = self.ptn_model.npn
                surface2plot = self.ptn_model.surf_pattern_neg_side 
                surface2plot1 = self.ptn_model.surf_pattern_pos_side 
            elif self.radio_scaled.isChecked() : 
                node2plot = self.ptn_expanded.npn
                surface2plot = self.ptn_expanded.surf_pattern_neg_side 
                surface2plot1 = self.ptn_expanded.surf_pattern_pos_side 
            elif self.radio_gauged.isChecked() : 
                node2plot = self.ptn_gauged.npn
                surface2plot = self.ptn_gauged.surf_pattern_neg_side 
                surface2plot1 = self.ptn_gauged.surf_pattern_pos_side 
            elif self.radio_bended.isChecked() : 
                node2plot = self.ptn_bended.npn
                surface2plot = self.ptn_bended.surf_pattern_neg_side 
                surface2plot1 = self.ptn_bended.surf_pattern_pos_side 
            else : 
                node2plot = self.ptn_bottomed.npn 
                surface2plot = self.ptn_bottomed.surf_pattern_neg_side 
                surface2plot1 = self.ptn_bottomed.surf_pattern_pos_side 
            if len(surface2plot) > 0: 
                self.figure.plot_surface(surface2plot, node2plot, search=self.searchsolid, surf_side=surface2plot1, number=number, position_shift=1)
                # self.message.setText("Pattern Side Surface has been plotted.")
                self.ShowingImage = 'pattern'
            else: 
                print ("No Pitch side surface")
        except:
            # self.message.setText("Pattern Side Surface has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'

    ## overlay plot ###########################
    def showMainGrvBtm(self):        ## Main Groove Bottom Surface
        if self.ShowingImage == 'pattern':
            self.searchsolid = self.SearchedSolids(id=1) 
            if self.checkBox_OverlaySurfNo.isChecked():  number = 1
            else: number = 0 
            try:
                surface2plot = self.ptn_model.SF_fulldepthgroove 
                grv_side = self.ptn_model.SF_fulldepthgrooveside
                if self.radio_model.isChecked() : 
                    node2plot = self.ptn_model.npn
                elif self.radio_scaled.isChecked() : 
                    node2plot = self.ptn_expanded.npn
                elif self.radio_gauged.isChecked() : 
                    node2plot = self.ptn_gauged.npn
                elif self.radio_bended.isChecked() : 
                    node2plot = self.ptn_bended.npn
                else : 
                    node2plot = self.ptn_bottomed.npn 
                if len(surface2plot) > 0:
                    # self.figure.plot_surface(surface2plot,node2plot, search=self.searchsolid, number=number, surf_side=grv_side, Second_plot=0)
                    self.figure.Add_surface(sf1=surface2plot, nodes=node2plot, search=self.searchsolid, number=number, sf2=grv_side)
                    # self.message.setText("Main Groove Bottom Surface has been plotted.")
                else: 
                    print ("No Groove bottom surface")
            except:
                # self.message.setText("Main Groove Bottom Surface has not been plotted.")
                self.figure.plot(show='none')
    def showSubGrvBtm(self):         ## Sub Groove Bottom Surface
        if self.ShowingImage == 'pattern':
            self.searchsolid = self.SearchedSolids(id=1) 
            if self.checkBox_OverlaySurfNo.isChecked():  number = 1
            else: number = 0 
            try:
                surface2plot = self.ptn_model.SF_subgroove 
                grv_side = self.ptn_model.SF_subgrooveside
                if self.radio_model.isChecked() : 
                    node2plot = self.ptn_model.npn
                elif self.radio_scaled.isChecked() : 
                    node2plot = self.ptn_expanded.npn
                elif self.radio_gauged.isChecked() : 
                    node2plot = self.ptn_gauged.npn
                elif self.radio_bended.isChecked() : 
                    node2plot = self.ptn_bended.npn
                else : 
                    node2plot = self.ptn_bottomed.npn 
                if len(surface2plot) > 0: 
                    # self.figure.plot_surface(surface2plot, node2plot, search=self.searchsolid, number=number, surf_side=grv_side)
                    self.figure.Add_surface(sf1=surface2plot, nodes=node2plot, search=self.searchsolid, number=number, sf2=grv_side)
                    # self.message.setText("Sub Groove Bottom Surface has been plotted.")
                else: 
                    print ("No Groove bottom surface")
            except:
                # self.message.setText("Sub Groove Bottom Surface has not been plotted.")
                self.figure.plot(show='none')
    def showMainGroove(self):  ## Pattern full depth groove Surface 
        if self.ShowingImage == 'pattern':
            self.searchsolid = self.SearchedSolids(id=1) 
            if self.checkBox_OverlaySurfNo.isChecked():  number = 1
            else: number = 0 
            try:
                surface2plot = self.ptn_model.beforeside 
                if self.radio_model.isChecked() : 
                    node2plot = self.ptn_model.npn
                elif self.radio_scaled.isChecked() : 
                    node2plot = self.ptn_expanded.npn
                elif self.radio_gauged.isChecked() : 
                    node2plot = self.ptn_gauged.npn
                elif self.radio_bended.isChecked() : 
                    node2plot = self.ptn_bended.npn
                else : 
                    node2plot = self.ptn_bottomed.npn 
                if len(surface2plot) > 0: 
                    self.figure.Add_surface(sf2=surface2plot, nodes=node2plot, search=self.searchsolid, number=number)
                    # self.message.setText("Pattern full depth groove Surface has been plotted.")
                else: 
                    print ("No Groove Side surface")
            except:
                # self.message.setText("Pattern full depth groove Surface has not been plotted.")
                self.figure.plot(show='none')
    def showSubGroove(self):   ## Pattern sub groove side Surface
        if self.ShowingImage == 'pattern':
            self.searchsolid = self.SearchedSolids(id=1) 
            if self.checkBox_OverlaySurfNo.isChecked():  number = 1
            else: number = 0 
            try:
                surface2plot = self.ptn_model.KerfsideSurface 
                if self.radio_model.isChecked() : 
                    node2plot = self.ptn_model.npn
                elif self.radio_scaled.isChecked() : 
                    node2plot = self.ptn_expanded.npn
                elif self.radio_gauged.isChecked() : 
                    node2plot = self.ptn_gauged.npn
                elif self.radio_bended.isChecked() : 
                    node2plot = self.ptn_bended.npn
                else : 
                    node2plot = self.ptn_bottomed.npn 
                if len(surface2plot) > 0: 
                    self.figure.Add_surface(sf2=surface2plot, nodes=node2plot, search=self.searchsolid, number=number)
                    # self.message.setText("Pattern sub groove side Surface has been plotted.")
                else: 
                    print ("No Groove Side surface")
            except:
                # self.message.setText("Pattern sub groove side Surface has not been plotted.")
                self.figure.plot(show='none')

    ### #########################################
    def showmodel(self): 
        self.searchsolid = self.SearchedSolids(id=1) 
        try:

            if self.radioTop.isChecked() : 
                self.showTopSurface()
                plotted =  1
            elif self.radioBottom.isChecked() : 
                self.showBottomSurface()
                plotted =  1
            elif self.radioPitch.isChecked() : 
                self.showPitch()
                plotted =  1
            elif self.radioSide.isChecked() :
                self.showSide()
                plotted =  1
            else: 
                self.showDefault()
            self.ShowingImage = 'pattern'
        except:
            # self.message.setText("Model Pattern has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showexpanded(self): 
        self.searchsolid = self.SearchedSolids(id=1) 
        try:
            if self.radioTop.isChecked() : 
                self.showTopSurface()
                plotted =  1
            elif self.radioBottom.isChecked() : 
                self.showBottomSurface()
                plotted =  1
            elif self.radioPitch.isChecked() : 
                self.showPitch()
                plotted =  1
            elif self.radioSide.isChecked() :
                self.showSide()
                plotted =  1
            else: 
                self.showDefault()
            self.ShowingImage = 'pattern'
        except:
            # self.message.setText("Scaled Pattern has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showgauged(self): 
        self.searchsolid= self.SearchedSolids(id=1) 
        try:
            if self.radioTop.isChecked() : 
                self.showTopSurface()
                plotted =  1
            elif self.radioBottom.isChecked() : 
                self.showBottomSurface()
                plotted =  1
            elif self.radioPitch.isChecked() : 
                self.showPitch()
                plotted =  1
            elif self.radioSide.isChecked() :
                self.showSide()
                plotted =  1
            else: 
                self.showDefault()
            self.ShowingImage = 'pattern'
        except:
            # self.message.setText("Gauge Adjusted Pattern has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showbended(self): 
        self.searchsolid= self.SearchedSolids(id=1) 
        try:
            if self.radioTop.isChecked() : 
                self.showTopSurface()
                plotted =  1
            elif self.radioBottom.isChecked() : 
                self.showBottomSurface()
                plotted =  1
            elif self.radioPitch.isChecked() : 
                self.showPitch()
                plotted =  1
            elif self.radioSide.isChecked() :
                self.showSide()
                plotted =  1
            else: 
                self.showDefault()
            self.ShowingImage = 'pattern'
        except:
            # self.message.setText("Bended Pattern has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'
    def showbottomed(self): 
        self.searchsolid = self.SearchedSolids(id=1) 
        try:
            if self.radioTop.isChecked() : 
                self.showTopSurface()
                plotted =  1
            elif self.radioBottom.isChecked() : 
                self.showBottomSurface()
                plotted =  1
            elif self.radioPitch.isChecked() : 
                self.showPitch()
                plotted =  1
            elif self.radioSide.isChecked() :
                self.showSide()
                plotted =  1
            else: 
                self.showDefault()
            self.ShowingImage = 'pattern'
        except:
            # self.message.setText("Expanded Pattern has not been plotted.")
            self.figure.plot(show='none')
            self.ShowingImage = 'none'

class myCanvas(FigureCanvas):
    def __init__(self, parent=None, *args, **kwargs):
        self.figure = plt.figure()
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,self)  

        # self.pos=[]
        self.p1=[]
        self.p2=[]
        self.distance = 0.0 
        self.clicked = 0 
        self.totalLength =0.0
        
        self.dots=[]
        self.lines=[]
        self.chars=[]
        self.achars=[]
        self.cline=[]
        self.llen=[]
        self.fontsize =  8

        self.mclick=0
        self.circle=[]

        self.surfs=[]
        self.texts=[]

        self.pointx =[]
        self.pointy = []
        self.points = []

        self.cxs=[]
        self.cys=[]

        self.lxs=[]
        self.lys=[]

        self.snap_mode = 1 

        self.Plot3D = 0 

    def zoom(self, event, base_scale=1.2): 
        
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()

        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location

        if event.button == 'down':
            # deal with zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'up':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print (event.button)

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        try: 
            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            #and set limits
            plt.xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            plt.ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
        except:
            pass 
        self.figure.canvas.draw_idle()

    def onclick(self, event): 
        if event.dblclick: 
            if event.button == 1: 
                self.snap_mode *= -1 
                if self.snap_mode == 1: print (" >> Snap Mode ON")
                else: print (" >> Snap Mode OFF")

    def onReleased(self, event): 
        
        if self.Plot3D == 0 : 
            if event.button == 2: 
                self.mclick += 1

                if self.snap_mode == 1 : #and self.mclick < 4: 
                    ind = []
                    indx1 = np.where(self.points[:,2]>=event.xdata-0.01)[0]
                    indx2 = np.where(self.points[:,2]<=event.xdata+0.01)[0]
                    indx = np.intersect1d(indx1, indx2)
                    if len(indx) > 0: 
                        indy1 = np.where(self.points[:,3]>=event.ydata-0.01)[0]
                        indy2 = np.where(self.points[:,3]<=event.ydata+0.01)[0]
                        indy = np.intersect1d(indy1, indy2)
                        if len(indy) > 0: 
                            ind = np.intersect1d(indx, indy) 
                    if len(ind) > 0 : 
                        mn = []
                        for ix in ind: 
                            l = sqrt( (event.xdata - self.points[ix][2])**2 + (event.ydata - self.points[ix][3])**2 )
                            mn.append([ix, l])
                        mn = np.array(mn)
                        lmin = np.min(mn[:,1]) 
                        lx = -1
                        for l in mn: 
                            if l[1] == lmin: 
                                lx = int(l[0])
                                break 
                        if lx >=0: 
                            tx = self.points[lx][2]
                            ty = self.points[lx][3]
                            # print ("B2", self.points[lx])
                    else: 
                        self.mclick -= 1
                        return 
                else:
                    tx = event.xdata
                    ty = event.ydata 


                if self.mclick == 4: 
                    self.cxs=[]
                    self.cys=[]
                    self.mclick=0
                    for dot in self.dots:
                        dot.remove()
                    self.dots=[]

                    for char in self.chars: 
                        char.set_visible(False)

                    for cl in self.circle:
                        cl.remove()

                    self.circle=[]
                
                elif self.mclick ==3:
                    
                    sameposition = 0 
                    for p1, p2 in zip(self.cxs, self.cys): 
                        if p1 == tx and p2 == ty: 
                            sameposition = 1 
                            break 
                    if sameposition == 1: 
                        self.mclick -= 1 
                        return 
                    else:  
                        self.cxs.append(tx)
                        self.cys.append(ty)

                        d, = plt.plot(tx, ty, 'o', color='gray')
                        self.dots.append(d)
                        

                        x1 = self.cxs[0]; x2=self.cxs[1]; x3=self.cxs[2]
                        y1 = self.cys[0]; y2=self.cys[1]; y3=self.cys[2]
                        A = x1*(y2-y3) - y1 *(x2-x3) + x2*y3 - x3*y2
                        B = (x1*x1 + y1*y1)*(y3-y2) +(x2**2 + y2**2)*(y1-y3) + (x3**2+y3**2)*(y2-y1)
                        C = (x1**2 + y1**2)*(x2-x3)+(x2**2+y2**2)*(x3-x1) + (x3*x3 + y3*y3)*(x1-x2)
                        D = (x1*x1 + y1*y1)*(x3*y2-x2*y3)+(x2*x2+y2*y2)*(x1*y3-x3*y1)+(x3*x3+y3*y3)*(x2*y1-x1*y2)
                        SQRT = B*B + C*C - 4*A*D  

                        # print ("A", A)
                        # print ("B", B)
                        # print ("C", C)
                        # print ("D", D)
                        # print ("S", SQRT)

                        if A == 0 or SQRT < 0.0: 
                            print (" The 3 nodes cannot make a circle.")
                            print (" (%10.3E, %10.3E), (%10.3E, %10.3E)\n (%10.3E, %10.3E)"%(self.cxs[0]*1000,self.cys[0]*1000, self.cxs[1]*1000,self.cys[1]*1000, self.cxs[2]*1000,self.cys[2]*1000))

                            for dot in self.dots:
                                dot.remove()
                            self.dots=[]
                            self.cxs=[]
                            self.cys=[]
                            self.mclick=0

                        else: 
                            cx = -B/A/2.0
                            cy = -C/A/2.0
                            
                            R = sqrt(SQRT) / 2/abs(A)

                            self.cxs.append(tx)
                            self.cys.append(ty)
                            d, = plt.plot(cx, cy, 'o', color='red')
                            self.dots.append(d)

                            
                            ch = plt.text((self.cxs[0]+self.cxs[1])/2.0, (self.cys[0]+self.cys[1])/2.0, "R="+str(round(R*1000, 2)), size=self.fontsize, color='black')
                            self.chars.append(ch)

                            if R > 1E10: 
                                print (" The circle cannot be drawn.")
                                print (" Center = %.3E, %.3E"%(-B/A*500, -C/A*500))
                                print (" Radius = %.3E"%(sqrt(SQRT) /abs(A)*500))
                            else: 
                                crcl = plt.Circle((cx, cy), R, color='gray', fill=False)
                                self.ax.add_artist(crcl)
                                self.circle.append(crcl)
                        self.mclick = 0 
                        self.cxs=[]
                        self.cys=[]
                            

                else:
                    sameposition = 0 
                    for p1, p2 in zip(self.cxs, self.cys): 
                        if p1 == tx and p2 == ty: 
                            sameposition = 1 
                            break 
                    if sameposition == 1: 
                        self.mclick -= 1 
                    else: 
                        self.cxs.append(tx)
                        self.cys.append(ty)

                        d, = plt.plot(tx, ty, 'o', color='gray')
                        self.dots.append(d)


                self.figure.canvas.draw_idle()

            elif event.button == 1: 


                self.clicked =0  
                self.mclick = 0
                self.cxs=[]
                self.cys=[]
                self.lxs=[]
                self.lys=[]

                for dot in self.dots: 
                    dot.remove()
                for line in self.lines: 
                    line.remove()
                for char in self.chars: 
                    char.set_visible(False)
                for char in self.achars: 
                    char.set_visible(False)
                for cl in self.cline: 
                    cl.remove()
                for ch in self.llen:
                    ch.set_visible(False)
                for cl in self.circle:
                    cl.remove()

                self.circle=[]

                self.dots=[]
                self.lines=[]
                self.chars=[]
                self.achars=[]

                self.cline=[]
                self.llen=[]

                self.figure.canvas.draw_idle()

            elif event.button ==3:
                self.clicked += 1
                if self.clicked ==1: self.totalLength = 0 

                if self.snap_mode == 1: 
                    # indx = min(np.searchsorted(self.pointx, event.xdata), len(self.pointx)-1)
                    ind = []
                    indx1 = np.where(self.points[:,2]>=event.xdata-0.01)[0]
                    indx2 = np.where(self.points[:,2]<=event.xdata+0.01)[0]
                    indx = np.intersect1d(indx1, indx2)
                    if len(indx) > 0: 
                        indy1 = np.where(self.points[:,3]>=event.ydata-0.01)[0]
                        indy2 = np.where(self.points[:,3]<=event.ydata+0.01)[0]
                        indy = np.intersect1d(indy1, indy2)
                        if len(indy) > 0: 
                            ind = np.intersect1d(indx, indy) 
                    if len(ind) > 0 : 
                        mn = []
                        for ix in ind: 
                            l = sqrt( (event.xdata - self.points[ix][2])**2 + (event.ydata - self.points[ix][3])**2 )
                            mn.append([ix, l])
                        mn = np.array(mn)
                        lmin = np.min(mn[:,1]) 
                        lx = -1
                        for l in mn: 
                            if l[1] == lmin: 
                                lx = int(l[0])
                                break 
                        if lx >=0: 
                            tx = self.points[lx][2]
                            ty = self.points[lx][3]
                            # print ("B3", self.points[lx])
                    else: 
                        tx = event.xdata; ty = event.ydata 

                        
                else: 
                    tx = event.xdata; ty = event.ydata

                prev = 0 
                for xs,ys in zip(self.lxs, self.lys): 
                    if tx == xs and ty == ys: 
                        prev = 1 
                        break 
                if prev == 1: 
                    self.clicked -= 1
                    return 

                self.lxs.append(tx)
                self.lys.append(ty)
                
                d, = plt.plot(tx, ty, 'o', color='red')
                self.dots.append(d)
                N = len(self.lxs)-1
                
                if N> 0: 
                    self.distance = round( sqrt((self.lxs[N]-self.lxs[N-1])**2 + (self.lys[N]-self.lys[N-1])**2 ) *1000, 2)
                    ch = plt.text((self.lxs[N]+self.lxs[N-1])/2.0, (self.lys[N]+self.lys[N-1])/2.0, str(self.distance), color="black", size=self.fontsize)
                    self.chars.append(ch)
                    self.totalLength += self.distance

                    ln, = plt.plot([self.lxs[N-1], self.lxs[N]],[self.lys[N-1], self.lys[N]], color='orange')
                    self.lines.append(ln)

                    if self.clicked > 2: 

                        sx = 0; sy=0
                        for x, y in zip(self.lxs, self.lys): 
                            sx += x
                            sy += y
                        cx = sx/(float(N)+1)
                        cy = sy/(float(N)+1)

                        area = self.Area(ix=self.lxs, iy=self.lys)
                        for achar in self.achars: 
                            achar.set_visible(False)
                        self.figure.canvas.draw_idle()
                        ach= plt.text(cx, cy, "A="+ str(round(area*1_000_000, 1)), color='gray', size=self.fontsize)
                        self.achars.append(ach)

                        for char in self.llen:
                            char.set_visible(False)

                        for line in self.cline: 
                            line.remove()
                        self.cline=[]
                        
                        self.distance = round( sqrt((self.lxs[N]-self.lxs[0])**2 + (self.lys[N]-self.lys[0])**2 ) *1000, 2)
                        ch = plt.text((self.lxs[N]+self.lxs[0])/2.0, (self.lys[N]+self.lys[0])/2.0, str(self.distance), color='gray', size=self.fontsize)
                        self.llen.append(ch)

                        ln, = plt.plot([self.lxs[0], self.lxs[N]],[self.lys[0], self.lys[N]], color='gray', linestyle="--" )
                        self.cline.append(ln)
                        n1 = [0, 0, self.lxs[N], self.lys[N]]
                        n2 = [0, 0, self.lxs[N-1], self.lys[N-1]]
                        n3 = [0, 0, self.lxs[N-2], self.lys[N-2]]
                        print ("  Angle =%.3f (Length sum=%.3f)"%(PTN.Angle_3nodes(n1, n2, n3)*180.0/3.14159, self.totalLength))

                self.figure.canvas.draw_idle()

    def Area(self, ix=[], iy=[]): 
        x =[]; y=[]
        for px, py in zip(ix, iy):
            x.append(px)
            y.append(py)
        x.append(ix[0]); y.append(iy[0])

        A = [0.0, 0.0, 0.0]

        n = len(x)-1

        for i in range(n):
            s = x[i] * y[i + 1] - x[i + 1] * y[i]
            A[0] += s
            A[1] += (x[i] + x[i + 1]) * s
            A[2] += (y[i] + y[i + 1]) * s

        A[0] = A[0] / 2.0


        return A[0]

    def plot(self, layout=[], pattern=[], show='layout', layoutNo=0, search=[], flattened_tread=[], ptn_elset=[], bended=1, add2d=[]): 
        ## add2d >> only 2d layout element number(s)
        self.Plot3D = 0 
        for pt in self.texts: 
            pt.set_visible(False)
        try: 
            for py in self.surfs: 
                py.remove()
        except:
            pass
        # MeshLineWidth = 0.3

        self.points = []

        MembWidth = 0.5
        Mcolor = 'red'
        shadow = 'gray'
        colordepth = 0.5 
        linewidth=0.1
        linecolor = 'black'
        fontsize = 6

        colors = [ 'tomato', 'royalblue', 'black', 'lightblue','lightgreen']
        colN = len(colors)

        plt.clf()
        self.figure.clear()
        if show.lower() == 'none': 
            minx = -1.0; maxx = 1.0
            miny = -1.0; maxy = 1.0

        if show.lower()=='layout' or show.lower() == 'all': 
            x= 2; y=3
            self.figure.clear()
            self.ax = self.figure.add_subplot(111)
            self.ax.axis('equal')

            npn = np.array(layout.Node.Node)
            elem = layout.Element.Element 
            poly = []
            for el in layout.Element.Element : 
                ix = np.where(npn[:,0]==el[1])[0][0]; n1= npn[ix]
                ix = np.where(npn[:,0]==el[2])[0][0]; n2= npn[ix]
                if el[6] == 3: 
                    ix = np.where(npn[:,0]==el[3])[0][0]; n3= npn[ix]
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=Color(el[5]), alpha=colordepth, lw=linewidth, ec=linecolor)
                elif el[6] == 4: 
                    ix = np.where(npn[:,0]==el[3])[0][0]; n3= npn[ix]
                    ix = np.where(npn[:,0]==el[4])[0][0]; n4= npn[ix]
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=Color(el[5]), alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color=Mcolor, alpha=colordepth, lw=linewidth*5, ec=Mcolor)

                if layoutNo == 1: 
                    if el[5] == "CTR" or el[5] == "CTB" or el[5] == "UTR" or el[5] == "SUT" or el[5] == "TRW" or el[5] == "BSW" or el[5] == "BTT": 
                        self.ax.text(n1[x], n1[y], str(int(n1[0])),  fontsize=fontsize, color='gray')
                        self.ax.text(n2[x], n2[y], str(int(n2[0])), fontsize=fontsize, color='gray')
                        self.ax.text(n3[x], n3[y], str(int(n3[0])),  fontsize=fontsize, color='gray')
                        if el[6] ==4: 
                            self.ax.text(n4[x], n4[y], str(int(n4[0])), fontsize=fontsize, color='gray')
                            cx = (n1[x]+n2[x]+n3[x]+n4[x])/4.0
                            cy = (n1[y]+n2[y]+n3[y]+n4[y])/4.0
                        else: 
                            cx = (n1[x]+n2[x]+n3[x])/3.0
                            cy = (n1[y]+n2[y]+n3[y])/3.0
                        self.ax.text(cx, cy, str(int(el[0])), fontsize=fontsize, color='darkblue')

                self.ax.add_patch(polygon)

            if len(add2d)>0: 
                for en in add2d: 
                    for el in layout.Element.Element: 
                        if en == el[0]: 
                            ix = np.where(npn[:,0]==el[1])[0][0]; n1= npn[ix]
                            ix = np.where(npn[:,0]==el[2])[0][0]; n2= npn[ix]
                            if el[6] == 3: 
                                ix = np.where(npn[:,0]==el[3])[0][0]; n3= npn[ix]
                                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color='black', alpha=colordepth, lw=linewidth, ec=linecolor)
                            elif el[6] == 4: 
                                ix = np.where(npn[:,0]==el[3])[0][0]; n3= npn[ix]
                                ix = np.where(npn[:,0]==el[4])[0][0]; n4= npn[ix]
                                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color='black', alpha=colordepth, lw=linewidth, ec=linecolor)
                            else: 
                                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color='black', alpha=colordepth, lw=linewidth*5, ec='black')
                            self.ax.add_patch(polygon)
                            break 

            ## Draw TIEs

            if len(layout.TieMaster) > 0: 
                for i, edge in enumerate(layout.TieMaster) : 
                    
                    ix = np.where(npn[:,0]==edge[0])[0][0]; n1= npn[ix]
                    ix = np.where(npn[:,0]==edge[1])[0][0]; n2= npn[ix]

                    plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], linewidth=2.0, color='white')

                    for j, slave in enumerate(layout.TieSlave[i]): 
                        ix = np.where(npn[:,0]==slave[0])[0][0]; n1= npn[ix]
                        ix = np.where(npn[:,0]==slave[1])[0][0]; n2= npn[ix]
                        
                        if j < colN: 
                            pj = j 
                        else: 
                            pj = j % colN 
                        slavecolor = colors[pj]

                        plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], linewidth=0.8, color=slavecolor)

            if len(layout.Press) > 0: 
                for i, edge in enumerate(layout.Press) : 
                    ix = np.where(npn[:,0]==edge[0])[0][0]; n1= npn[ix]
                    ix = np.where(npn[:,0]==edge[1])[0][0]; n2= npn[ix]
                    plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], linewidth=0.5, color='black', ls='--')
            if len(layout.RimContact) > 0: 
                for i, edge in enumerate(layout.RimContact) : 
                    ix = np.where(npn[:,0]==edge[0])[0][0]; n1= npn[ix]
                    ix = np.where(npn[:,0]==edge[1])[0][0]; n2= npn[ix]
                    plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], linewidth=0.5, color='tomato', ls="--")
            if len(flattened_tread) > 0: 
                nx = flattened_tread[:,x]
                ny = flattened_tread[:,y] + 50E-03
                plt.scatter(nx, ny, c='lightgray', marker='o', edgecolor=None, s=1.0)


            rx = npn[:,x]; ry = npn[:,y]
            minx = np.min(rx); maxx = np.max(rx)
            miny = np.min(ry); maxy = np.max(ry)

            self.points = npn 

            del(npn)

        if show.lower()=='pattern':
            
            # if search > 0: 
            #     if search < 10**7: search += 10**7 

            x= 2; y=1
            self.figure.clear()
            self.ax = self.figure.add_subplot(111)
            self.ax.axis('equal')
            
            
            npn = pattern.npn
            surface = pattern.Free_Surface_without_BTM
            btmcolor='gray'

            sfnd = []

            color_searched = 'red'
            px=[]; py=[]
            for sf in surface: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix]
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix]
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix]
                px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
                py.append(n1[y]); py.append(n2[y]); py.append(n3[y]); 

                sfnd.append([n1[0], 0.0, n1[x], n1[y]]); sfnd.append([n2[0], 0.0, n2[x], n2[y]]); sfnd.append([n3[0], 0.0, n3[x], n3[y]])
                
                fd = 0 
                for sc in search: 
                    if sc == sf[0]: 
                        fd =1
                        break 
                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]; py.append(n4[y])
                    sfnd.append([n4[0], 0.0, n4[x], n4[y]])
                    
                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                self.ax.add_patch(polygon) 
            
            surface = pattern.freetop
            topcolor='aqua'
            
            for sf in surface: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix]
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix]
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix]
                px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
                py.append(n1[y]); py.append(n2[y]); py.append(n3[y]); 
                sfnd.append([n1[0], 0.0, n1[x], n1[y]]); sfnd.append([n2[0], 0.0, n2[x], n2[y]]); sfnd.append([n3[0], 0.0, n3[x], n3[y]])

                fd = 0 
                for sc in search: 
                    if sc == sf[0]: 
                        fd =1
                        break 

                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]; py.append(n4[y])
                    sfnd.append([n4[0], 0.0, n4[x], n4[y]])

                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=topcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=topcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                self.ax.add_patch(polygon)

            rx = npn[:,x]; ry = npn[:,y]
            minx = np.min(rx); maxx = np.max(rx)
            miny = np.min(ry); maxy = np.max(ry)

            btmcolor='gray'

            l1 = len(pattern.surf_pitch_down)
            l2 = len(pattern.surf_pitch_up)
            if l1 < l2: surface = pattern.surf_pitch_down
            else: surface = pattern.surf_pitch_up

            rz = npn[:,3]
            R = np.max(rz) 
            
            shift = miny - 10.0E-03 -R 
            x=2; y=3 
            nx = []
            ht = [] 
            for sf in surface: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
                ht.append(n1[1])
                px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
                py.append(n1[y]+ shift); py.append(n2[y]+ shift); py.append(n3[y]+ shift); 

                sfnd.append([n1[0], 0.0, n1[x], n1[y]+ shift]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+ shift]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+ shift])


                fd = 0 
                for sc in search: 
                    if sc == sf[0]: 
                        fd =1
                        break 

                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix] ; py.append(n4[y]+ shift)
                    sfnd.append([n4[0], 0.0, n4[x], n4[y]+ shift])
                    
                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                self.ax.add_patch(polygon) 

            ht = np.array(ht)
            minht = np.min(ht)

            shift = maxy + 10.0E-03 - minht

            x=2; y=1 
            nx = []
            for sf in surface: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
                nx.append(n1[y] + shift)
                px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
                py.append(n1[y]+ shift); py.append(n2[y]+ shift); py.append(n3[y]+ shift); 

                sfnd.append([n1[0], 0.0, n1[x], n1[y]+ shift]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+ shift]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+ shift])

                fd = 0 
                for sc in search: 
                    if sc == sf[0]: 
                        fd =1
                        break 
                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix] ; py.append(n4[y]+ shift)
                    sfnd.append([n4[0], 0.0, n4[x], n4[y]+ shift])
                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    if fd == 1 :
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=color_searched, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
                self.ax.add_patch(polygon) 
            
            nx = np.array(nx)
            maxy = np.max(nx)

            px= np.array(px); py = np.array(py)
            minx = np.min(px); maxx = np.max(px)
            miny = np.min(py); maxy = np.max(py)

            self.points = np.array(sfnd)

            del(px)
            del(py)
            del(nx)
            del(surface)
            
        if show.lower()=='all': 
            surface = pattern.surf_pitch_down
            npn = pattern.npn

            sfnd = []

            pointx=[]; pointy=[]
            
            btmcolor='orange'
            sutcolor='pink'
            x=2; y=3 
            rs = []
            sut = [] 
            if len(ptn_elset) > 0: 
                for eset in ptn_elset: 
                    if eset[0] =="SUT" or eset[0] =="UTR": 
                        sut = eset[1]
                        break 
            if len(sut) > 0: 
                sut = np.array(sut) 

            for sf in surface: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix]
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix]
                try:
                    ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
                except:
                    print(sf[7],",", sf[8],",", sf[9])
                

                
                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix] 
                

                    if bended ==1: 
                        r1 = sqrt(n1[1]**2 + n1[3]**2); r2 = sqrt(n2[1]**2 + n2[3]**2); r3 = sqrt(n3[1]**2 + n3[3]**2); r4 = sqrt(n4[1]**2 + n4[3]**2); 
                    else: 
                        r1 = n1[3]; r2 = n2[3]; r3=n3[3]; r4 = n4[3]

                    sfnd.append([n1[0], 0.0, n1[2], r1])
                    sfnd.append([n2[0], 0.0, n2[2], r2])
                    sfnd.append([n3[0], 0.0, n3[2], r3])
                    sfnd.append([n4[0], 0.0, n4[2], r4])

                    rs.append(r1); rs.append(r2); rs.append(r3); rs.append(r4) 
                    el_color = btmcolor
                    if len(sut) > 0: 
                        if len(np.where(sut == sf[0])[0]) > 0:  el_color = sutcolor 
                    
                    polygon = plt.Polygon([[n1[x], r1], [n2[x], r2], [n3[x], r3], [n4[x], r4]], color=el_color, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    if bended == 1: 
                        r1 = sqrt(n1[1]**2 + n1[3]**2); r2 = sqrt(n2[1]**2 + n2[3]**2); r3 = sqrt(n3[1]**2 + n3[3]**2)
                    else: 
                        r1 = n1[3]; r2 = n2[3]; r3=n3[3]
                    
                    sfnd.append([n1[0], 0.0, n1[2], r1])
                    sfnd.append([n2[0], 0.0, n2[2], r2])
                    sfnd.append([n3[0], 0.0, n3[2], r3])

                    rs.append(r1); rs.append(r2); rs.append(r3)
                    el_color = btmcolor
                    if len(sut) > 0: 
                        if len(np.where(sut == sf[0])[0]) > 0:  el_color = sutcolor 
                        
                    polygon = plt.Polygon([[n1[x], r1], [n2[x], r2], [n3[x], r3]], color=el_color, alpha=colordepth, lw=linewidth, ec=linecolor)
                self.ax.add_patch(polygon) 
            rs = np.array(rs)
            maxy = np.max(rs)

            ix = np.where(npn[:,0]<10**7+10000)[0]
            nx =[]; ny=[]
            for k in ix: 
                nx.append(npn[k][2])
                if bended ==1: 
                    r = sqrt(npn[k][1]**2 + npn[k][3]**2)
                else: 
                    r = npn[k][3]
                ny.append(r)
                # allx.append(npn[k][2]); ally.append(r)
            plt.scatter(nx, ny, c='gray', marker='o', edgecolor=None, s=.50)
            # allx=np.array(allx); ally=np.array(ally)
            # plt.scatter(allx, ally, c='lightgray', edgecolor=None, s=0.01)

            if show.lower()=='all' :
                self.points = np.concatenate((self.points, np.array(sfnd)), axis=0) 

            else: 
                self.points = npn 

            del(nx)
            del(ny)
            del(rs)
            del(npn)
            del(surface)
            
        try:
            plt.xlim(minx-0.01, maxx+0.01)
            plt.ylim(miny-0.01, maxy+0.01)
        except:
            print ("Image range")
            print ("X %.3f~%.3f"%(minx*1000, maxx*1000))
            print ("Y %.3f~%.3f"%(miny*1000, maxy*1000))

        # print (" all printed node =%d"%(len(self.points)))

        self.figure.canvas.mpl_connect('button_release_event', self.onReleased)
        self.figure.canvas.mpl_connect('scroll_event',self.zoom)
        self.figure.canvas.mpl_connect('button_press_event', self.onclick)

        self.figure.tight_layout()
        self.figure.canvas.draw()
                    
    def plot_error(self, solids, nodes): 
        plt.clf()
        self.figure.clear()
        # self.ax = self.figure.add_subplot(1,1,1, projection='3d')
        self.ax = Axes3D(self.figure)

        self.Plot3D = 1 
        
        X = []
        Y = []
        Z = []
        for solid in solids: 
            self.ax, lm = AddSolidon3DPlot(self.ax, solid, nodes)
            for x in lm[0]: 
                X.append(x)
            for x in lm[1]: 
                Y.append(x)
            for x in lm[2]: 
                Z.append(x)
        X = np.array(X)
        Y = np.array(Y)
        Z = np.array(Z)

        X = X.reshape(1, -1)
        Y = Y.reshape(1, -1)
        Z = Z.reshape(1, -1)
            
        delX = np.max(X)-np.min(X)
        delY = np.max(Y)-np.min(Y)
        delZ = np.max(Z)-np.min(Z)
        avgX = (np.max(X)+np.min(X))/2.0
        avgY = (np.max(Y)+np.min(Y))/2.0
        avgZ = (np.max(Z)+np.min(Z))/2.0

        diff = np.array([delX, delY, delZ])
        maxd = np.max(diff) 
            

        # Get rid of the panes
        self.ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        # Get rid of the spines
        self.ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

        # Get rid of the ticks
        # self.ax.set_xticks([]) 
        # self.ax.set_yticks([]) 
        # self.ax.set_zticks([])
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.set_xlim3d(avgX - maxd, avgX + maxd)
        self.ax.set_ylim3d(avgY - maxd, avgY + maxd)
        self.ax.set_zlim3d(avgZ - maxd, avgZ + maxd)
        # self.figure.tight_layout()
        self.figure.canvas.draw()

    def plot_pitch_surface(self, sfup, sfdown, nodes, R=0, search=[], number = 0, downpos=0, uppos=0): 

        for pt in self.texts: 
            pt.set_visible(False)
        try: 
            for py in self.surfs: 
                py.remove()
        except:
            pass

        color = 'gray'
        transparency = 0.5
        textcolor = 'black'
        textsize = 8
        linewidth = 0.1
        edgecolor = 'black'
        searched_color = 'orange'

        sfnd = []

        plt.clf()
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('equal')

        x = 2; y=3 
        shift = uppos - R 

        px = []; py=[]
        for sf in sfup: 
            ix = np.where(nodes[:,0] == sf[7])[0][0]; n1 = nodes[ix]
            ix = np.where(nodes[:,0] == sf[8])[0][0]; n2 = nodes[ix]
            ix = np.where(nodes[:,0] == sf[9])[0][0]; n3 = nodes[ix]
            px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
            py.append(n1[y]+shift); py.append(n2[y]+shift); py.append(n3[y]+shift); 

            sfnd.append([n1[0], 0.0, n1[x], n1[y]+shift]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+shift]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+shift])
            
            if sf[10] > 10: 
                ix = np.where(nodes[:,0] == sf[10])[0][0]; n4 = nodes[ix]; py.append(n4[y]+shift)
                sfnd.append([n4[0], 0.0, n4[x], n4[y]+shift])

                polygon = plt.Polygon([[n1[x], n1[y]+shift], [n2[x], n2[y]+shift], [n3[x], n3[y]+shift], [n4[x], n4[y]+shift]], \
                    color=color, alpha=transparency, lw=linewidth, ec=edgecolor)
            else: 
                polygon = plt.Polygon([[n1[x], n1[y]+shift], [n2[x], n2[y]+shift], [n3[x], n3[y]+shift]], \
                    color=color, alpha=transparency, lw=linewidth, ec=edgecolor)

            self.ax.add_patch(polygon)
            if number == 1: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 +shift , str(int(sf[0]-10**7)), size=textsize, color=textcolor)

        shift = downpos - R 
        for sf in sfdown: 
            ix = np.where(nodes[:,0] == sf[7])[0][0]; n1 = nodes[ix]
            ix = np.where(nodes[:,0] == sf[8])[0][0]; n2 = nodes[ix]
            ix = np.where(nodes[:,0] == sf[9])[0][0]; n3 = nodes[ix]
            px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
            py.append(n1[y]+shift); py.append(n2[y]+shift); py.append(n3[y]+shift); 

            sfnd.append([n1[0], 0.0, n1[x], n1[y]+shift]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+shift]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+shift])
            
            if sf[10] > 10: 
                ix = np.where(nodes[:,0] == sf[10])[0][0]; n4 = nodes[ix]; py.append(n4[y]+shift)
                sfnd.append([n4[0], 0.0, n4[x], n4[y]+shift])

                polygon = plt.Polygon([[n1[x], n1[y]+shift], [n2[x], n2[y]+shift], [n3[x], n3[y]+shift], [n4[x], n4[y]+shift]], \
                    color=color, alpha=transparency, lw=linewidth, ec=edgecolor)
            else: 
                polygon = plt.Polygon([[n1[x], n1[y]+shift], [n2[x], n2[y]+shift], [n3[x], n3[y]+shift]], \
                    color=color, alpha=transparency, lw=linewidth, ec=edgecolor)

            self.ax.add_patch(polygon)
            if number == 1: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 +shift , str(int(sf[0]-10**7)), size=textsize, color=textcolor)

        px= np.array(px); py = np.array(py)
        minx = np.min(px); maxx = np.max(px)
        miny = np.min(py); maxy = np.max(py)
        

        plt.xlim(minx-0.01, maxx+0.01)
        plt.ylim(miny-0.01, maxy+0.01)

        self.points = np.array(sfnd)

        self.figure.canvas.mpl_connect('button_release_event', self.onReleased)

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def plot_surface(self, surface, nodes, search=[], layout_points=[], top_lines=[], surf_side=[], number=0, position_shift=0, Second_plot=0):
        for pt in self.texts: 
            pt.set_visible(False)
        try: 
            for py in self.surfs: 
                py.remove()
        except:
            pass
        # if search > 0: print ("search the no of pattern element =%d"%(search))

        # MeshLineWidth = 0.3
        # MembWidth = 0.5
        Mcolor = 'red'
        shadow = 'gray'
        colordepth = 0.5 
        linewidth=0.1
        linecolor = 'black'

        btmcolor='gray'

        edge_line_color = 'red'
        edge_line_width = 0.5 
        EdgeBoundary = SurfaceBoundary(surface) 

        npn = nodes
        sfnd = []
        
        plt.clf()
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('equal')
        

        x= 2; y=1
        
        topcolor='aqua'

        searched_color = 'red'
        # if search < 10**7: search += 10**7 
        
        px = []; py=[]
        for sf in surface: 
            ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix]
            ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix]
            ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix]
            px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
            py.append(n1[y]); py.append(n2[y]); py.append(n3[y]); 

            sfnd.append([n1[0], 0.0, n1[x], n1[y]]); sfnd.append([n2[0], 0.0, n2[x], n2[y]]); sfnd.append([n3[0], 0.0, n3[x], n3[y]])

            fd = 0 
            for sc in search: 
                if sc == sf[0]: 
                    fd =1
                    break 
            if sf[10] > 10: 
                ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]; py.append(n4[y])
                sfnd.append([n4[0], 0.0, n4[x], n4[y]])
                if fd ==1 : 
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=searched_color, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=topcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
            else: 
                if fd == 1:
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=searched_color, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=topcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
            self.ax.add_patch(polygon)
            if number == 1: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 , str(int(sf[0]-10**7)), size=8, color='b')


        if len(surf_side)>0 : 
            btm1color = 'orange'
            for sf in surf_side: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix]
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix]
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix]
                px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
                py.append(n1[y]); py.append(n2[y]); py.append(n3[y]); 
                sfnd.append([n1[0], 0.0, n1[x], n1[y]]); sfnd.append([n2[0], 0.0, n2[x], n2[y]]); sfnd.append([n3[0], 0.0, n3[x], n3[y]])

                fd = 0 
                for sc in search: 
                    if sc == sf[0]: 
                        fd =1
                        break 
                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]; py.append(n4[y])
                    sfnd.append([n4[0], 0.0, n4[x], n4[y]])

                    if fd ==1  : 
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=searched_color, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=btm1color, alpha=colordepth, lw=linewidth, ec=linecolor)
                else: 
                    if fd ==1 :
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=searched_color, alpha=colordepth, lw=linewidth, ec=linecolor)
                    else: 
                        polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=btm1color, alpha=colordepth, lw=linewidth, ec=linecolor)
                self.ax.add_patch(polygon)
                if number == 1: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 , str(int(sf[0]-10**7)), size=8, color='b')

        for edge in EdgeBoundary: 
            ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
            ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color=edge_line_color, alpha=1.0, lw=edge_line_width, ec=edge_line_color)
            self.ax.add_patch(polygon)

        rx = npn[:,x]; ry = npn[:,y]
        minx = np.min(rx); maxx = np.max(rx)
        miny = np.min(ry); maxy = np.max(ry)

        btmcolor='gray'

            
        rz = npn[:,3]
        R = np.max(rz) 
        
        shift = miny - 10.0E-03 -R 
        x=2; y=3 
        nx = []
        ht = [] 
        
        for sf in surface: 
            ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
            ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
            ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
            nx.append(n1[y] + shift)
            ht.append(n1[3])
            

            px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
            py.append(n1[y]+ shift); py.append(n2[y]+ shift); py.append(n3[y]+ shift); 

            sfnd.append([n1[0], 0.0, n1[x], n1[y]+shift]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+shift]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+shift])

            if sf[10] > 10: 
                ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]; py.append(n4[y]+ shift)
                sfnd.append([n4[0], 0.0, n4[x], n4[y]+shift])

                polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
            else: 
                polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
            self.ax.add_patch(polygon) 
            if number == 2: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 + shift, str(int(sf[0]-10**7)), size=8, color='b')

        if len(surf_side)>0 : 
            btm1color = 'orange'
            colordepth1 = 0.5
            linecolor_r = 'red'
            for sf in surf_side: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
                nx.append(n1[y] + shift)
                ht.append(n1[3])

                px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
                py.append(n1[y]+ shift); py.append(n2[y]+ shift); py.append(n3[y]+ shift); 
                sfnd.append([n1[0], 0.0, n1[x], n1[y]+shift]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+shift]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+shift])

                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]; py.append(n4[y]+ shift)
                    sfnd.append([n4[0], 0.0, n4[x], n4[y]+shift])

                    polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=btm1color, alpha=colordepth1, lw=linewidth, ec=linecolor_r)
                else: 
                    polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=btm1color, alpha=colordepth1, lw=linewidth, ec=linecolor_r)
                self.ax.add_patch(polygon) 

                if number == 2: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 + shift, str(int(sf[0]-10**7)), size=8, color='b')


        for edge in EdgeBoundary: 
            ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
            ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color=edge_line_color, alpha=1.0, lw=edge_line_width, ec=edge_line_color)
            self.ax.add_patch(polygon)

        if len(layout_points) > 0 :
            lx=[]; ly=[]
            for nd in layout_points: 
                lx.append(nd[x])
                ly.append(nd[y]+shift)
            plt.scatter(lx, ly, color='gray', s=2.0)
        if len(top_lines) > 0:
            for ln in top_lines: 
                plt.plot(ln[0], ln[1]+shift, color="red", linewidth=0.1) 



        nx = np.array(nx)
        miny = np.min(nx)

        ht = np.array(ht)
        # maxht = np.max(ht)
        minht = np.min(ht)

        shift = maxy + 10.0E-03 - minht

        x=1; y=3 
        # nx = []
        suby=[] 
        for sf in surface: 
            ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
            ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
            ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
            # nx.append(n1[y] + shift)
            px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
            py.append(n1[y]+ shift); py.append(n2[y]+ shift); py.append(n3[y]+ shift); 

            sfnd.append([n1[0], 0.0, n1[x], n1[y]+shift]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+shift]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+shift])

            suby.append(n1[y]+shift)

            if sf[10] > 10: 
                ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix];  py.append(n4[y]+ shift)
                sfnd.append([n4[0], 0.0, n4[x], n4[y]+shift])

                polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
            else: 
                polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
            self.ax.add_patch(polygon) 
            if number == 3: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 + shift, str(int(sf[0]-10**7)), size=8, color='b')

        if len(surf_side)>0 : 
            btm1color = 'orange'
            colordepth1 = 0.5
            linecolor_r = 'gray'
            suby = np.array(suby)
            if position_shift == 1:    ty = np.max(suby) - np.min(suby) + 5.0E-03
            else:             ty = 0  
            for sf in surf_side: 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
                # nx.append(n1[y] + shift )
                px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
                py.append(n1[y]+ shift- ty); py.append(n2[y]+ shift- ty); py.append(n3[y]+ shift- ty); 
                sfnd.append([n1[0], 0.0, n1[x], n1[y]+shift- ty]); sfnd.append([n2[0], 0.0, n2[x], n2[y]+shift- ty]); sfnd.append([n3[0], 0.0, n3[x], n3[y]+shift- ty])

                if sf[10] > 10: 
                    ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix];  py.append(n4[y]+ shift- ty)
                    sfnd.append([n4[0], 0.0, n4[x], n4[y]+shift- ty])
                    polygon = plt.Polygon([[n1[x], n1[y] + shift- ty], [n2[x], n2[y] + shift- ty], [n3[x], n3[y] + shift- ty], [n4[x], n4[y] + shift- ty]], color=btm1color, alpha=colordepth1, lw=linewidth, ec=linecolor_r)
                else: 
                    polygon = plt.Polygon([[n1[x], n1[y] + shift- ty], [n2[x], n2[y] + shift- ty], [n3[x], n3[y] + shift- ty]], color=btm1color, alpha=colordepth1, lw=linewidth, ec=linecolor_r)
                self.ax.add_patch(polygon) 
                if number == 3: self.ax.text((n1[x]+n2[x]+n3[x])/3, (n1[y]+n2[y]+n3[y])/3.0 + shift- ty, str(int(sf[0]-10**7)), size=8, color='b')
        
        for edge in EdgeBoundary: 
            ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
            ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color=edge_line_color, alpha=1.0, lw=edge_line_width, ec=edge_line_color)
            self.ax.add_patch(polygon)
            # plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], color=edge_line_color, linewidth=edge_line_width)

        
        px= np.array(px); py = np.array(py)
        minx = np.min(px); maxx = np.max(px)
        miny = np.min(py); maxy = np.max(py)
        

        plt.xlim(minx-0.01, maxx+0.01)
        plt.ylim(miny-0.01, maxy+0.01)

        self.points = np.array(sfnd)

        # lineprops = {"color":"blue", "linewidth": 1.0, "alpha": 0.1}
        # lasso = LassoSelector(self.ax, self.onSelect, button=[2])
        # self.figure.canvas.mpl_connect('button_press_event', self.onPressed)
        self.figure.canvas.mpl_connect('button_release_event', self.onReleased)

        self.figure.tight_layout()
        self.figure.canvas.draw()
        # print(" Surface was plotted (No of the surfaces=%d)"%(len(surface) + len(surf_side)))

    def Add_layer(self, plane, np2, solid, np3): 
        for pt in self.texts: 
            pt.set_visible(False)
        try: 
            for py in self.surfs: 
                py.remove()
        except:
            pass

        textsize = 8
        textcolor = 'black'
        eltxtcolor = 'red' 
        self.surfs =[]
        self.texts = []
        facecolor = 'orange'
        faceedgecolor = 'gray'
        alphs = 1.0 
        lw = 0.5 
        x = 2; y=3 

        if len(plane) > 0: 
            for pn in plane : 
                ix = np.where(np2[:,0] == pn[1])[0][0]; n1=np2[ix]
                t = self.ax.text(np2[ix][x], np2[ix][y], str(int(np2[ix][0])), size=textsize, color=textcolor); self.texts.append(t)
                ix = np.where(np2[:,0] == pn[2])[0][0]; n2=np2[ix]
                t = self.ax.text(np2[ix][x], np2[ix][y], str(int(np2[ix][0])), size=textsize, color=textcolor); self.texts.append(t)

                if pn[3] == 0: 
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color=facecolor, alpha=1.0, lw=lw, ec=facecolor)
                    tx = (n1[x]+n2[x])/2.0
                    ty = (n1[y]+n2[y])/2.0

                elif pn[4] == 0: 
                    ix = np.where(np2[:,0] == pn[3])[0][0]; n3=np2[ix]
                    t = self.ax.text(np2[ix][x], np2[ix][y],  str(int(np2[ix][0])), size=textsize, color=textcolor); self.texts.append(t)
                    polygon = plt.Polygon([ [n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=facecolor, alpha=1.0, lw=lw, ec=faceedgecolor)
                    tx = (n1[x]+n2[x]+n3[x])/3.0
                    ty = (n1[y]+n2[y]+n3[y])/3.0
                else: 
                    ix = np.where(np2[:,0] == pn[3])[0][0]; n3=np2[ix]
                    t = self.ax.text(np2[ix][x], np2[ix][y],  str(int(np2[ix][0])), size=textsize, color=textcolor); self.texts.append(t)
                    ix = np.where(np2[:,0] == pn[4])[0][0]; n4=np2[ix]
                    t = self.ax.text(np2[ix][x], np2[ix][y],  str(int(np2[ix][0])), size=textsize, color=textcolor); self.texts.append(t)
                    polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=facecolor, alpha=1.0, lw=lw, ec=faceedgecolor)
                    tx = (n1[x]+n2[x]+n3[x])/3.0
                    ty = (n1[y]+n2[y]+n3[y])/3.0
                
                self.ax.add_patch(polygon)
                self.surfs.append(polygon)
                t = self.ax.text(tx, ty, str(int(pn[0])), size=textsize, color=eltxtcolor)
                self.texts.append(t)

        
        if len(solid) > 0: 
            for pn in solid : 
                ix = np.where(np3[:,0] == pn[1])[0][0]; n1=np3[ix]
                ix = np.where(np3[:,0] == pn[2])[0][0]; n2=np3[ix]
                ix = np.where(np3[:,0] == pn[3])[0][0]; n3=np3[ix]
                ix = np.where(np3[:,0] == pn[4])[0][0]; n4=np3[ix]
                ix = np.where(np3[:,0] == pn[5])[0][0]; n5=np3[ix]
                ix = np.where(np3[:,0] == pn[6])[0][0]; n6=np3[ix]
                if pn[8]> 0: 
                    ix = np.where(np3[:,0] == pn[7])[0][0]; n7=np3[ix]
                    ix = np.where(np3[:,0] == pn[8])[0][0]; n8=np3[ix]

                    polygon1 = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n6[x], n6[y]], [n5[x], n5[y]]], color=facecolor, alpha=1.0, lw=lw, ec=faceedgecolor)
                    polygon2 = plt.Polygon([[n2[x], n2[y]], [n3[x], n3[y]], [n7[x], n7[y]], [n6[x], n6[y]]], color=facecolor, alpha=1.0, lw=lw, ec=faceedgecolor)
                    tx = (n1[x]+n2[x]+n3[x]+n4[x]+n5[x]+n6[x]+n7[x]+n8[x])/8.0
                    ty = (n1[y]+n2[y]+n3[y]+n4[y]+n5[y]+n6[y]+n7[y]+n8[y])/8.0
                else: 
                    polygon1 = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n5[x], n5[y]], [n4[x], n4[y]]], color=facecolor, alpha=1.0, lw=lw, ec=faceedgecolor)
                    polygon2 = plt.Polygon([[n2[x], n2[y]], [n3[x], n3[y]], [n6[x], n6[y]], [n5[x], n5[y]]], color=facecolor, alpha=1.0, lw=lw, ec=faceedgecolor)

                    tx = (n1[x]+n2[x]+n3[x]+n4[x]+n5[x]+n6[x])/6.0
                    ty = (n1[y]+n2[y]+n3[y]+n4[y]+n5[y]+n6[y])/6.0
                t = self.ax.text(tx, ty, str(int(pn[0]-10**7)), size=textsize, color=eltxtcolor)
                self.texts.append(t)

                self.ax.add_patch(polygon1)
                self.surfs.append(polygon1)
                self.ax.add_patch(polygon2)
                self.surfs.append(polygon2)


        self.figure.canvas.draw_idle()

    def Add_surface(self, sf1=[], sf2=[], nodes=[], number=0, sf3=[], sf4=[], search=[], boundary=0, \
        sf1color='orange', sf2color='violet', sf3color='green', sf4color='navy'): 
        for pt in self.texts: 
            pt.set_visible(False)
        try: 
            for py in self.surfs: 
                py.remove()
        except:
            pass

        self.surfs =[]
        self.texts = []
        textsize = 8
        textcolor = 'black'        

        if len(sf1)> 0: 
            surface = sf1 
            color = sf1color
            poly, texts = surface_polygon(surface=surface, nodes=nodes, search=search, number=number, boundary=boundary, color=color)
            for py in poly: 
                self.ax.add_patch(py)
                self.surfs.append(py)
            if number == 1: 
                for txt in texts: 
                    t = self.ax.text(txt[1], txt[2], txt[0], size=textsize, color=textcolor)
                    self.texts.append(t)

        if len(sf2)> 0: 
            surface = sf2 
            color = sf2color
            poly, texts = surface_polygon(surface=surface, nodes=nodes, search=search, number=number, boundary=boundary, color=color)
            for py in poly: 
                self.ax.add_patch(py)
                self.surfs.append(py)
            if number == 1: 
                for txt in texts: 
                    t = self.ax.text(txt[1], txt[2], txt[0], size=textsize, color=textcolor)
                    self.texts.append(t)
        if len(sf1)> 0: 
            surface = sf3 
            color = sf3color
            poly, texts = surface_polygon(surface=surface, nodes=nodes, search=search, number=number, boundary=boundary, color=color)
            for py in poly: 
                self.ax.add_patch(py)
                self.surfs.append(py)
            if number == 1: 
                for txt in texts: 
                    t = self.ax.text(txt[1], txt[2], txt[0], size=textsize, color=textcolor)
                    self.texts.append(t)
        if len(sf1)> 0: 
            surface = sf4  
            color = sf4color
            poly, texts = surface_polygon(surface=surface, nodes=nodes, search=search, number=number, boundary=boundary, color=color)
            for py in poly: 
                self.ax.add_patch(py)
                self.surfs.append(py)
            if number == 1: 
                for txt in texts: 
                    t = self.ax.text(txt[1], txt[2], txt[0], size=textsize, color=textcolor)
                    self.texts.append(t)


        self.figure.canvas.draw_idle()
                

def Color(elsetname):                ## Define Color set 
    c = ''
    if elsetname == 'CTR' or elsetname == 'CTB':
        c = 'darkgray'
    elif elsetname == 'UTR' or elsetname == 'SUT':
        c = 'lightpink'
    elif elsetname == 'CC1' or elsetname == 'C01' or elsetname == 'C02':
        c = 'lightsalmon'
    elif elsetname == 'CCT':
        c = 'purple'
    elif elsetname == 'BTT':
        c = 'steelblue'
    elif elsetname == 'FIL' or elsetname == 'LBF':
        c = 'green'
    elif elsetname == 'UBF':
        c = 'lightpink'
    elif elsetname == 'IL1' or elsetname == 'L11':
        c = 'y'
    elif elsetname == 'BSW':
        c = 'yellowgreen'
    elif elsetname == 'HUS':
        c = 'steelblue'
    elif elsetname == 'RIC':
        c = 'darkgray'
    elif elsetname == 'SHW':
        c = 'darkcyan'
    elif elsetname == 'BD1':
        c = 'dimgray'
    elif elsetname == 'BDC':
        c = 'black'
    elif elsetname == 'MEMB':
        c = 'black'
    elif elsetname == 'DOT':
        c = 'red'
    elif elsetname == 'PRESS':
        c = 'blue'
    elif elsetname == 'RIM':
        c = 'red'
    elif elsetname == 'TDBASE':
        c = 'aqua'
    elif elsetname == 'TDROAD':
        c = 'coral'
    elif elsetname == 'BDTOP':
        c = 'gray'
    else:
        c = 'silver'
    return c


def writeworkingdirectory(readfile, dfile='pdir.dir'): 
    cwd=''
    drs = readfile.split("/")
    for i, dr in enumerate(drs): 
        cwd += dr + '/'
        if i == len(drs) -2 : break 
    f= open(dfile, "w")
    f.write(cwd)
    f.close()

    return cwd 

def writestatus(dfile="status.sta", new=0, **kwargs): 
    if new == 1: 
        f=open(dfile, 'w')
        f.write("%d, %d, %d, %d, %d"%(0, 0, 0, 0, 0))
        f.close()
    else: 
        with open(dfile) as IN:
            line = IN.readlines()
        state = list(line[0].split(","))
        shoR = int(state[0])
        t3d = int(state[1])
        sut  = int(state[2])
        rev  = int(state[3])
        if len(state) > 4: abq = int(state[4])
        else: abq = 0 
        
        # negSho=0, T3DM=0, SUT=0, Rev=0,
        for key, val in kwargs.items(): 
            if key == 'negSho': shoR = val 
            if key == 'T3DM':  t3d = val 
            if key == 'SUT':  sut = val 
            if key == 'Rev':  rev = val 
            if key == 'ABQ': abq = val 

        f=open(dfile, 'w')
        f.write("%d, %d, %d, %d, %d"%(shoR, t3d, sut, rev, abq))
        f.close()


def surface_polygon(surface=[], nodes=[], search=[], number=0, \
    linewidth=0.1, edgecolor='black', color='orange', boundary=1, searchedcolor='red', colordepth=0.5) : 
    x = 2; y=1
    npn = nodes 
    polygons=[]
    texts = []

    px=[]; py=[]

    for sf in surface: 
        ix = np.where(npn[:,0] == sf[7])[0][0]
        n1 = npn[ix]
        ix = np.where(npn[:,0] == sf[8])[0][0]
        n2 = npn[ix]
        ix = np.where(npn[:,0] == sf[9])[0][0]
        n3 = npn[ix]
        px.append(n1[x]); px.append(n2[x]); px.append(n3[x]); 
        py.append(n1[y]); py.append(n2[y]); py.append(n3[y]); 
        fd = 0 
        for sc in search: 
            if sc == sf[0]: 
                fd =1
                break 
        if sf[10] > 10: 
            ix = np.where(npn[:,0] == sf[10])[0][0]
            n4 = npn[ix]
            py.append(n4[y])
            if fd ==1 : 
                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=searchedcolor, alpha=colordepth, lw=linewidth, ec=edgecolor)
            else: 
                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=color, alpha=colordepth, lw=linewidth, ec=edgecolor)
        else: 
            if fd == 1:
                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=searchedcolor, alpha=colordepth, lw=linewidth, ec=edgecolor)
            else: 
                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=color, alpha=colordepth, lw=linewidth, ec=edgecolor)
        polygons.append(polygon)

        texts.append([str(int(sf[0]-10**7)), (n1[x]+n2[x]+n3[x])/3.0, (n1[y]+n2[y]+n3[y])/3.0 ])

    if boundary == 1: 
        edge_line_color = 'red'
        edge_line_width = 0.5 
        boundary = SurfaceBoundary(surface) 
        for edge in boundary: 
            ix = np.where(npn[:,0] == edge[0])[0][0]; 
            n1 = npn[ix]
            ix = np.where(npn[:,0] == edge[1])[0][0]
            n2 = npn[ix]

            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color=edge_line_color, alpha=1.0, lw=edge_line_width, ec=edge_line_color)
            polygons.append(polygon)

    return polygons, texts 

def AddSurfacePlot(ax, surface, nodes): 
    # MeshLineWidth = 0.3
    MembWidth = 0.5
    Mcolor = 'red'
    shadow = 'gray'
    colordepth = 0.5 
    linewidth=0.1
    linecolor = 'black'

    npn = nodes
    btmcolor='gray'

    edge_line_color = 'red'
    edge_line_width = 0.5 

    EdgeBoundary = SurfaceBoundary(surface) 

    for sf in surface: 
        ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix]
        ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix]
        ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix]
        if sf[10] > 10: 
            ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        else: 
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        ax.add_patch(polygon) 

    for edge in EdgeBoundary: 
        ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
        ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
        plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], color=edge_line_color, linewidth=edge_line_width)

    
    
    topcolor='aqua'
    
    for sf in surface: 
        ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix]
        ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix]
        ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix]
        if sf[10] > 10: 
            ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix]
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], color=topcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        else: 
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]]], color=topcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        ax.add_patch(polygon)

    for edge in EdgeBoundary: 
        ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
        ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
        plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], color=edge_line_color, linewidth=edge_line_width)


    rx = npn[:,x]; ry = npn[:,y]
    minx = np.min(rx); maxx = np.max(rx)
    miny = np.min(ry); maxy = np.max(ry)

    btmcolor='gray'

        
    rz = npn[:,3]
    R = np.max(rz) 
    
    shift = miny - 10.0E-03 -R 
    x=2; y=3 
    nx = []
    ht = [] 
    for sf in surface: 
        ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
        ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
        ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
        nx.append(n1[y] + shift)
        ht.append(n1[1])
        if sf[10] > 10: 
            ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix] 
            polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        else: 
            polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        ax.add_patch(polygon) 

    for edge in EdgeBoundary: 
        ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
        ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
        plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], color=edge_line_color, linewidth=edge_line_width)


    nx = np.array(nx)
    miny = np.min(nx)

    ht = np.array(ht)
    # maxht = np.max(ht)
    minht = np.min(ht)

    shift = maxy + 1.0E-03 - minht

    x=2; y=1 
    nx = []
    for sf in surface: 
        ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
        ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
        ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
        nx.append(n1[y] + shift)
        if sf[10] > 10: 
            ix = np.where(npn[:,0] == sf[10])[0][0]; n4 = npn[ix] 
            polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift], [n4[x], n4[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        else: 
            polygon = plt.Polygon([[n1[x], n1[y] + shift], [n2[x], n2[y] + shift], [n3[x], n3[y] + shift]], color=btmcolor, alpha=colordepth, lw=linewidth, ec=linecolor)
        ax.add_patch(polygon) 

    for edge in EdgeBoundary: 
        ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
        ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
        plt.plot ([n1[x], n2[x]], [n1[y], n2[y]], color=edge_line_color, linewidth=edge_line_width)
    
    nx = np.array(nx)
    maxy = np.max(nx)

    return ax, minx, maxx, miny, maxy 


def AddSolidon3DPlot(ax, solid, nodes): 
    textsize = 9
    ix = np.where(nodes[:,0] == solid[1])[0]
    if len(ix) > 0: n1 = nodes[ix[0]]
    ix = np.where(nodes[:,0] == solid[2])[0]
    if len(ix) > 0: n2 = nodes[ix[0]]
    ix = np.where(nodes[:,0] == solid[3])[0]
    if len(ix) > 0: n3 = nodes[ix[0]]
    ix = np.where(nodes[:,0] == solid[4])[0]
    if len(ix) > 0: n4 = nodes[ix[0]]
    ix = np.where(nodes[:,0] == solid[5])[0]
    if len(ix) > 0: n5 = nodes[ix[0]]
    ix = np.where(nodes[:,0] == solid[6])[0]
    if len(ix) > 0: n6 = nodes[ix[0]]
    
    if solid[7] > 0: 
        ix = np.where(nodes[:,0] == solid[7])[0]
        if len(ix) > 0: n7 = nodes[ix[0]]
        ix = np.where(nodes[:,0] == solid[8])[0]
        if len(ix) > 0: n8 = nodes[ix[0]]

        X = [n1[1], n2[1], n3[1], n4[1], n5[1], n6[1], n7[1], n8[1]]
        Y = [n1[2], n2[2], n3[2], n4[2], n5[2], n6[2], n7[2], n8[2]]
        Z = [n1[3], n2[3], n3[3], n4[3], n5[3], n6[3], n7[3], n8[3]]
        ax.scatter([n1[1]], [n1[2]], [n1[3]], c='black', marker='o')
        ax.scatter([n2[1]], [n2[2]], [n2[3]], c='blue', marker='o')
        ax.scatter([n3[1]], [n3[2]], [n3[3]], c='green', marker='o')
        ax.scatter([n4[1]], [n4[2]], [n4[3]], c='red', marker='o')
        ax.scatter([n5[1]], [n5[2]], [n5[3]], c='black', marker='o')
        ax.scatter([n6[1]], [n6[2]], [n6[3]], c='blue', marker='o')
        ax.scatter([n7[1]], [n7[2]], [n7[3]], c='green', marker='o')
        ax.scatter([n8[1]], [n8[2]], [n8[3]], c='red', marker='o')
        ax.text(n1[1], n1[2], n1[3], str(int(n1[0]-10**7)), color='b', size=textsize)
        ax.text(n2[1], n2[2], n2[3], str(int(n2[0]-10**7)), color='black', size=textsize)
        ax.text(n3[1], n3[2], n3[3], str(int(n3[0]-10**7)), color='black', size=textsize)
        ax.text(n4[1], n4[2], n4[3], str(int(n4[0]-10**7)), color='black', size=textsize)
        ax.text(n5[1], n5[2], n5[3], str(int(n5[0]-10**7)), color='b', size=textsize)
        ax.text(n6[1], n6[2], n6[3], str(int(n6[0]-10**7)), color='black', size=textsize)
        ax.text(n7[1], n7[2], n7[3], str(int(n7[0]-10**7)), color='black', size=textsize)
        ax.text(n8[1], n8[2], n8[3], str(int(n8[0]-10**7)), color='black', size=textsize)

        cx = np.average(np.array(X)); cy = np.average(np.array(Y)); cz = np.average(np.array(Z))
        ax.text(cx, cy, cz, "["+str(int(solid[0]-10**7))+"]", color='r', size=textsize+2)

        
        lx = [n1[1], n2[1], n3[1], n4[1], n1[1]]
        ly = [n1[2], n2[2], n3[2], n4[2], n1[2]]
        lz = [n1[3], n2[3], n3[3], n4[3], n1[3]]
        ax.plot(lx, ly, lz, 'gray') 

        lx = [n1[1], n2[1], n3[1], n4[1]]
        ly = [n1[2], n2[2], n3[2], n4[2]]
        lz = [n1[3], n2[3], n3[3], n4[3]]
        verts = [list(zip(lx, ly, lz))]
        ax.add_collection3d(Poly3DCollection(verts, alpha=0.1, color='gray'), zs=lz)


        lx = [n5[1], n6[1], n7[1], n8[1], n5[1]]
        ly = [n5[2], n6[2], n7[2], n8[2], n5[2]]
        lz = [n5[3], n6[3], n7[3], n8[3], n5[3]]
        ax.plot(lx, ly, lz, 'b') 

        lx = [n5[1], n6[1], n7[1], n8[1]]
        ly = [n5[2], n6[2], n7[2], n8[2]]
        lz = [n5[3], n6[3], n7[3], n8[3]]
        verts = [list(zip(lx, ly, lz))]
        ax.add_collection3d(Poly3DCollection(verts, alpha=0.1, color='gray'), zs=lz)

        lx = [n1[1], n5[1]]
        ly = [n1[2], n5[2]]
        lz = [n1[3], n5[3]]
        ax.plot(lx, ly, lz, 'green', linestyle="--")
        lx = [n2[1], n6[1]]
        ly = [n2[2], n6[2]]
        lz = [n2[3], n6[3]]
        ax.plot(lx, ly, lz, 'green', linestyle="--")
        lx = [n3[1], n7[1]]
        ly = [n3[2], n7[2]]
        lz = [n3[3], n7[3]]
        ax.plot(lx, ly, lz, 'green', linestyle="--")
        lx = [n4[1], n8[1]]
        ly = [n4[2], n8[2]]
        lz = [n4[3], n8[3]]
        ax.plot(lx, ly, lz, 'green', linestyle="--")

    else: 
        X = [n1[1], n2[1], n3[1], n4[1], n5[1], n6[1]]
        Y = [n1[2], n2[2], n3[2], n4[2], n5[2], n6[2]]
        Z = [n1[3], n2[3], n3[3], n4[3], n5[3], n6[3]]

        # X = [n1[1], n2[1], n3[1], n4[1], n5[1], n6[1]]
        # Y = [n1[2], n2[2], n3[2], n4[2], n5[2], n6[2]]
        # Z = [n1[3], n2[3], n3[3], n4[3], n5[3], n6[3]]


        # ax.scatter(X, Y, Z, c='r', marker='o') 
        ax.scatter([n1[1]], [n1[2]], [n1[3]], c='black', marker='o')
        ax.scatter([n2[1]], [n2[2]], [n2[3]], c='blue', marker='o')
        ax.scatter([n3[1]], [n3[2]], [n3[3]], c='green', marker='o')

        ax.scatter([n4[1]], [n4[2]], [n4[3]], c='black', marker='o')
        ax.scatter([n5[1]], [n5[2]], [n5[3]], c='blue', marker='o')
        ax.scatter([n6[1]], [n6[2]], [n6[3]], c='green', marker='o')
        
        lx = [n1[1], n2[1], n3[1], n1[1]]
        ly = [n1[2], n2[2], n3[2], n1[2]]
        lz = [n1[3], n2[3], n3[3], n1[3]]
        ax.plot(lx, ly, lz, 'gray') 
        lx = [n1[1], n2[1], n3[1]]
        ly = [n1[2], n2[2], n3[2]]
        lz = [n1[3], n2[3], n3[3]]
        verts = [list(zip(lx, ly, lz))]
        ax.add_collection3d(Poly3DCollection(verts, alpha=0.1, color='gray'), zs=lz)


        lx = [n4[1], n5[1], n6[1], n4[1]]
        ly = [n4[2], n5[2], n6[2], n4[2]]
        lz = [n4[3], n5[3], n6[3], n4[3]]
        ax.plot(lx, ly, lz, 'b') 
        lx = [n4[1], n4[1], n4[1]]
        ly = [n5[2], n5[2], n5[2]]
        lz = [n6[3], n6[3], n6[3]]
        verts = [list(zip(lx, ly, lz))]
        ax.add_collection3d(Poly3DCollection(verts, alpha=0.1, color='gray'), zs=lz)


        lx = [n1[1], n4[1]]
        ly = [n1[2], n4[2]]
        lz = [n1[3], n4[3]]
        ax.plot(lx, ly, lz, 'green', linestyle="--")
        lx = [n2[1], n5[1]]
        ly = [n2[2], n5[2]]
        lz = [n2[3], n5[3]]
        ax.plot(lx, ly, lz, 'green', linestyle="--")
        lx = [n3[1], n6[1]]
        ly = [n3[2], n6[2]]
        lz = [n3[3], n6[3]]
        ax.plot(lx, ly, lz, 'green', linestyle="--")

        
        ax.text(n1[1], n1[2], n1[3], str(int(n1[0]-10**7)), color='b', size=textsize)
        ax.text(n2[1], n2[2], n2[3], str(int(n2[0]-10**7)), color='black', size=textsize)
        ax.text(n3[1], n3[2], n3[3], str(int(n3[0]-10**7)), color='black', size=textsize)
        ax.text(n4[1], n4[2], n4[3], str(int(n4[0]-10**7)), color='b', size=textsize)
        ax.text(n5[1], n5[2], n5[3], str(int(n5[0]-10**7)), color='black', size=textsize)
        ax.text(n6[1], n6[2], n6[3], str(int(n6[0]-10**7)), color='black', size=textsize)

        cx = np.average(np.array(X)); cy = np.average(np.array(Y)); cz = np.average(np.array(Z))
        ax.text(cx, cy, cz, "["+str(int(solid[0]-10**7))+"]", size=textsize+2)

    return ax, [X, Y, Z]

def SurfaceBoundary(surface):
    ## surface = [El_id, Face_Id(1~6), type(3 or 4), layer, center X, y, z, n1, n2, n3, n4]
    bndedge=[]
    alledge =[]
    for sf in surface:
        alledge.append([int(sf[7]), int(sf[8]), 0, sf[0]])
        alledge.append([int(sf[8]), int(sf[9]), 0, sf[0]])
        if sf[2] == 3: alledge.append([int(sf[9]), int(sf[7]), 0, sf[0]])
        else:
            alledge.append([int(sf[9]), int(sf[10]), 0, sf[0]])
            alledge.append([int(sf[10]), int(sf[7]), 0, sf[0]])

    npedge = np.array(alledge, dtype=np.int32)
    N = len(npedge)
    for i, eg in enumerate(npedge):
        if eg[2] == -1: continue
        bnd = 1

        ind1 = np.where(npedge[:, 1] == eg[0])
        if len(ind1[0]) > 0 : 
            N = len(ind1[0])
            for j in range(N):
                if npedge[ind1[0][j]][0] == eg[1]: 
                    npedge[i][2] = -1
                    bnd = 0 
                    break 
        if bnd ==1:
            npedge[i][2] =1
            bndedge.append(npedge[i])
    
    return np.array(bndedge)
if __name__ == "__main__":
    import sys

    # ftp = FTP.SSHClient()
    # ftp.set_missing_host_key_policy(FTP.AutoAddPolicy())
    # user = 'h20200155'
    # pw = 'h20200155'
    # try: 
    #     ftp.connect(host, username=user, password=pw)
    #     sftp = ftp.open_sftp()
    #     dirList =sftp.listdir(wdir)
    #     dirList = sorted(dirList)

    # except: pass 
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # MainWindow.showMaximized()
    # MainWindow.setWindowTitle("Pattern Mesh Expanding Tool for SMART")
    MainWindow.show()
    
    sys.exit(app.exec_())