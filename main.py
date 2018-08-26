#trial.py

import sys, os
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from variables import *
from auxilliary_functions import *
from shutil import copyfile
from subprocess import check_output
import time
import _thread
import subprocess

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.screenAdjust ()
        self.allText()
        self.title = 'Full chain CFD'
        self.allGeometriesPresent = False
        self.meshReady = False
        self.meshRunning = False
        self.carColor = redColor
        self.refBoxColor = redColor
        self.bndBoxColor = redColor
        self.initUI()
        self.geometryCheckModule()
        self.meshingModule()
        self.simulationModule()
        self.setAcceptDrops(True)
        self.updateButtonsOnTime(500)
        self.update()


        #TODO: handle reversal of tasks. Mesh was already present




    def initUI(self):
        self.setWindowTitle(self.title)
        # Insert domain image

        labelDomainImage = QLabel(self)
        pixmapDomainImage = QPixmap('GIMP_Domain.png')
        pixmapDomainImage = pixmapDomainImage.scaledToWidth(self.vis_domainImageWidth)
        labelDomainImage.setPixmap(pixmapDomainImage)
        labelDomainImage.move(self.vis_image_move_x, self.vis_image_move_y)

        self.show()

    def screenAdjust (self):

        ##GENERAL - Overal width, button sizes, image
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.screen_size = QDesktopWidget().screenGeometry()

        window_width = self.screen_size.width() / screen_fraction
        window_height = self.screen_size.height() / screen_fraction

        monitor_width = self.screen_size.width()
        monitor_height = self.screen_size.height()

        self.resize(window_width, window_height)

        self.GUIsize = self.geometry()

        self.move((monitor_width - window_width) / 2,
                      (monitor_height - window_height) / 2)
        self.vis_widthBoxDrop = window_height / (3)
        self.vis_heightBoxDrop = window_height / (3*6)

        self.vis_domainImageWidth = window_width / 1.2
        self.vis_StopImageWidth = window_width/ 20
        self.vis_image_move_x = (window_width - self.vis_domainImageWidth) / 2
        self.vis_image_move_y = window_height/(3*4)

        self.vis_input_box_width = window_width/20
        self.vis_input_box_height = window_height / 20

        self.vis_move_input_box_negative = 0#monitor_height/50
        #TODO: find out why there is a mismatch in height

        self.vis_stopButtonWidth = window_height/25

        self.vis_pushButtonHeight = window_height/15


        ############  WIDTH - General

        self.vis_one_third_x = window_width/ 3
        self.vis_two_third_x = window_width * 2 / 3
        self.vis_half_x = window_width/ 2
        self.vis_full_x = window_width
        self.vis_pushButtonWidth = window_width/5.5
        self.vis_StatusIndicator_x = window_width/4


        ############WIDTH - Geometry specific
        self.vis_before_title1_x = window_width/15
        self.vis_firstColumn1 = window_width / (3*2.25)
        self.vis_geoName_locs = window_width/ 17
        self.vis_geometry_button_x = window_width/(3*4.5)


        ###########WIDTH - Mesh specific
        self.vis_mesh_button_x  = self.vis_geometry_button_x/1.5 + self.vis_one_third_x
        self.vis_before_title2_x = window_width/2.5
        self.vis_meshName_locs = window_width/2.5
        self.vis_meshInputGap = window_width/6

        self.vis_meshStopButon = window_width/1.7

        ###########WIDTH - Simulation specific
        self.vis_simulation_button_x  = self.vis_mesh_button_x + self.vis_one_third_x
        self.vis_before_title3_x = window_width/2.5 + self.vis_one_third_x
        self.vis_simName_locs = window_width/2.5 + self.vis_one_third_x
        self.vis_simulationInputGap = self.vis_meshStopButon

        self.vis_simStopButon = window_width/1.7 + self.vis_one_third_x

        ###########HEIGHT - General
        self.vis_one_third_y = window_height / 3
        self.vis_two_third_y = window_height * 2 / 3
        self.vis_half_y = window_height / 2
        self.vis_full_y = window_height

        self.vis_StatusIndicator_y =   0*window_height*0.05



        ##########HEIGHT - Geoemtry specific
        self.vis_geo_heightLevel1 = window_height * 0.575
        self.vis_geo_heightLevel2 = window_height* 0.675
        self.vis_geo_heightLevel3 = window_height * 0.775

        self.vis_geometry_button_y = window_height*0.9

        ###HEIGHT - Mesh specific
        self.vis_mesh_heightLevel1 = window_height * 0.6
        self.vis_mesh_heightLevel2 = window_height * 0.7
        self.vis_mesh_heightLevel3 = window_height * 0.8
        self.vis_mesh_heightLevel4 = window_height * 0.9


        ###HEIGHT - Mesh specific
        self.vis_sim_heightLevel1 = window_height * 0.575
        self.vis_sim_heightLevel2 = window_height * 0.65
        self.vis_sim_heightLevel3 = window_height * 0.725
        self.vis_sim_heightLevel4 = window_height * 0.8

    def allText(self):
        self.text_geometryTitle = 'Check Geometry  '
        self.test_carName = 'Car'
        self.text_refinementBoxName = 'Refinement box'
        self.text_boundingBoxName = 'Bounding box'
        self.text_geometryCheckButton = 'Check if geometries exist'
        self.text_geometryCheckButtonTooltip = 'Searches Input_Files directory for geometries'

        self.text_meshTitle = 'Mesh Setup '
        self.text_meshStartButtonText = 'Start mesh generation'
        self.text_meshStartButtontooltip = 'This starts the mesh generation process'

        self.text_simulationTitle = 'Simulation Setup  '
        self.text_simStartButtonText = 'Start simulation'
        self.text_simStartButtontooltip = 'This starts the FINEOpen simulation'

        self.text_StatusBar = "STATUS: "
        self.text_Status_drop_geometries = "Drop the geometries with a drag-and-drop"
        self.text_Status_start_meshing = "Geometries are ready. Start the meshing"
        self.text_Status_start_simulation = "Mesh is ready. Start the simulation"
        self.text_Status_fully_completed = "The simulation has been performed. Check out the results"

        self.text_Bad = u'\u2717'
        self.text_Good = u'\u2713'

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)

        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, self.vis_half_y, self.vis_full_x, self.vis_half_y)
        qp.drawLine(self.vis_two_third_x, self.vis_half_y, self.vis_two_third_x, self.vis_full_y)
        qp.drawLine(self.vis_one_third_x, self.vis_half_y, self.vis_one_third_x, self.vis_full_y)

    def drawRectangles(self, qp, xcoord, ycoord, colorOfBox):
        qp.setBrush(QColor(colorOfBox))
        qp.drawRect(xcoord, ycoord, self.vis_widthBoxDrop, self.vis_heightBoxDrop)

    def geometryCheckModule(self):
        # Check geometry
        self.geometryCheckText = self.display_text(self, self.text_geometryTitle + self.text_Bad, self.vis_before_title1_x,
                                                   self.vis_half_y, LargeFont, LargeFontSize)

        self.carInput = self.draw_input_box(self.vis_geoName_locs, self.vis_geo_heightLevel1, 1, car_file_name, self.test_carName, self.carColor)
        self.refBoxInput = self.draw_input_box(self.vis_geoName_locs, self.vis_geo_heightLevel2, 2, refbox_file_name, self.text_refinementBoxName, self.refBoxColor)
        self.bndBoxInput = self.draw_input_box(self.vis_geoName_locs, self.vis_geo_heightLevel3, 3, bndbox_file_name, self.text_boundingBoxName, self.bndBoxColor)

        self.geometryCheckButton = QPushButtonWithExtraFeatures(self, self.text_geometryCheckButton , self.text_geometryCheckButtonTooltip,
                                          self.vis_pushButtonWidth, self.vis_pushButtonHeight, self.vis_geometry_button_x,
                                          self.vis_geometry_button_y )
        self.geometryCheckButton.clicked.connect(self.on_geo_check_click)

        self.statusText = self.display_text(self, self.text_StatusBar + self.text_Status_drop_geometries,
                                                   self.vis_StatusIndicator_x,
                                                   self.vis_StatusIndicator_y, LargeFont, LargeFontSize)

    def on_geo_check_click(self):
        self.carColor = color_return(car_file_name)
        self.refBoxColor = color_return(refbox_file_name)
        self.bndBoxColor = color_return(bndbox_file_name)

        self.carInput.setStyleSheet("background-color: "+self.carColor+";")
        self.refBoxInput.setStyleSheet("background-color: " + self.refBoxColor + ";")
        self.bndBoxInput.setStyleSheet("background-color: " + self.bndBoxColor + ";")

        print('In geometry check click')
        if self.carColor == greenColor and self.refBoxColor == greenColor and self.bndBoxColor == greenColor:
            self.allGeometriesPresent = True
            self.geometryCheckText.setText(self.text_geometryTitle + self.text_Good)
            self.meshButton.setEnabled(True)
            self.meshStopbutton.setEnabled(True)
            self.statusText.setText(self.text_StatusBar+ self.text_Status_start_meshing)
        else:
            self.allGeometriesPresent = False
            self.geometryCheckText.setText(self.text_geometryTitle + self.text_Bad)
            self.meshButton.setEnabled(False)
            self.meshStopbutton.setEnabled(False)
            self.statusText.setText(self.text_StatusBar+ self.text_Status_drop_geometries)


    def meshingModule(self):
        # Meshing setup
        self.meshCheckText = self.display_text(self, self.text_meshTitle + self.text_Bad, self.vis_before_title2_x,
                                                   self.vis_half_y, LargeFont, LargeFontSize)


        self.BaseHText = QLineEditWithInputValue(self, self.vis_meshName_locs, self.vis_mesh_heightLevel1, 'Cell Size in Domain', 0.5)
        self.refCarText = QLineEditWithInputValue(self, self.vis_meshName_locs, self.vis_mesh_heightLevel2, 'Refinements on car', 3)
        self.refBoxText = QLineEditWithInputValue(self, self.vis_meshName_locs, self.vis_mesh_heightLevel3, 'Refinements on \nrefinement box', 2)


        self.meshButton = QPushButtonWithExtraFeatures(self, self.text_meshStartButtonText , self.text_meshStartButtontooltip ,
                                          self.vis_pushButtonWidth, self.vis_pushButtonHeight, self.vis_mesh_button_x , self.vis_geometry_button_y)

        self.meshButton.clicked.connect(self.on_mesh_generation_click)

        self.meshStopbutton = QPushStopButton(self, self.vis_meshStopButon, self.vis_geometry_button_y)
        self.meshStopbutton.clicked.connect(lambda: self.handleStopButton(1))

        if self.allGeometriesPresent == False:
            self.meshButton.setEnabled(False)
            self.meshStopbutton.setEnabled(False)


    def on_mesh_generation_click(self):
        baseH = self.BaseHText.text()
        refCarRefinement = self.refCarText.text()
        refBoxRefinement = self.refBoxText.text()

        confLocation  = generateConfFile(baseH, refCarRefinement, refBoxRefinement)
        command_to_run = hybridPath + " "+confLocation +" -print"
        proc = subprocess.Popen([command_to_run], shell=True , preexec_fn = os.setsid)

        self.meshRunning = True
        self.is_meshing_complete()

    def is_meshing_complete(self):
        hex_file = meshing_directory+ meshName
        if os.path.exists(hex_file):
            self.meshReady = True
            self.simulationButton.setEnabled(True)
            self.simStopbutton.setEnabled(True)
            self.meshCheckText.setText(self.text_meshTitle + self.text_Good)
            self.statusText.setText(self.text_StatusBar+ self.text_Status_start_simulation)


        if not os.path.exists(hex_file):
            self.meshReady = False
            self.simulationButton.setEnabled(False)
            self.simStopbutton.setEnabled(False)
            self.meshCheckText.setText(self.text_meshTitle + self.text_Bad)





    def simulationModule(self):

        self.simulationTitleText = self.display_text(self, self.text_simulationTitle  + self.text_Bad, self.vis_simulation_button_x,
                                                     self.vis_half_y, LargeFont, LargeFontSize)

        self.simulationButton = QPushButtonWithExtraFeatures(self, self.text_simStartButtonText,
                                                            self.text_simStartButtontooltip,  self.vis_pushButtonWidth,
                                                            self.vis_pushButtonHeight, self.vis_simulation_button_x, self.vis_geometry_button_y)
        self.simulationButton.clicked.connect(self.on_simulation_button_click)

        self.simStopbutton = QPushStopButton(self, self.vis_simStopButon, self.vis_geometry_button_y)
        self.simStopbutton.clicked.connect(lambda: self.handleStopButton(2))

        self.inletVelText = QLineEditWithInputValue(self, self.vis_simName_locs, self.vis_sim_heightLevel1, 'Inlet Velocity', 25)
        self.turbIntensityText = QLineEditWithInputValue(self, self.vis_simName_locs, self.vis_sim_heightLevel2, 'Turbulence Intensity', '4%')
        self.liftDirText = QLineEditWithInputValue(self, self.vis_simName_locs, self.vis_sim_heightLevel3, 'Lift direction', 'X')
        self.dragDirText = QLineEditWithInputValue(self, self.vis_simName_locs, self.vis_sim_heightLevel4, 'Drag direction', 'Y')

        if self.meshReady == False:
            self.simulationButton.setEnabled(False)
            self.simStopbutton.setEnabled(False)
        elif self.meshReady == True:
            self.simulationButton.setEnabled(True)
            self.simStopbutton.setEnabled(True)

    @pyqtSlot()
    def on_simulation_button_click(self):
        inletVelocity = self.inletVelText.text()
        turbulenceIntensity = self.turbIntensityText.text()
        liftDirection = self.liftDirText.text()
        dragDirection = self.dragDirText.text()

        print(inletVelocity)
        print(turbulenceIntensity)
        print(liftDirection)
        print(dragDirection)


        pythonFOMacroLocation = generateSimulationMacro(inletVelocity, turbulenceIntensity, liftDirection, dragDirection)
        print(FOpath + " " + pythonFOMacroLocation)
        #MacroFOSetup = subprocess.Popen([FOpath + " -script " + pythonFOMacroLocation + " -batch"], shell=True , preexec_fn = os.setsid)
        check_output([FOpath + " -script " + pythonFOMacroLocation + " -batch"], shell=True , preexec_fn = os.setsid)


        print(simulationBat)
        if os.path.exists(simulationBat):
            SimulationProcess = subprocess.Popen([simulationBat], shell=True, preexec_fn=os.setsid)
        if not os.path.exists(simulationBat):
            raise ValueError('the FO macro did not work')

    def is_simulation_complete(self):
        if os.path.exists(simulationCFView):
            self.simulationReady = True
            self.simulationTitleText.setText(self.text_simulationTitle + self.text_Good)
            self.statusText.setText(self.text_StatusBar+ self.text_Status_fully_completed)


        if not os.path.exists(hex_file):
            self.simulationReady = True


    def handleStopButton(self, n):
        if n== 1:
            process = "hexpresshybridx86_64"
            #TODO: Very badly implemented. Get PID somehwo
        if n==2:
            process = "hexstreamdpx86_64"

        os.system("pkill -f "+process)


    def display_text(self, parent, toPrint, whereX, whereY, fontStyle, fontSize):
        disp_text = QLabel(parent)
        disp_text.setText(toPrint)
        disp_text.move(whereX, whereY)
        disp_text.setFont(QFont(fontStyle, fontSize))
        disp_text.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        return disp_text

    def draw_input_box(self, coordx, coordy, boxNumber, file_name, nameToPrint, color):
        input_box = QLineEditWithDrop('', self, boxNumber, file_name, nameToPrint, MediumFont, MediumFontSize)
        input_box.setDragEnabled(True)
        input_box.resize(self.vis_widthBoxDrop, self.vis_heightBoxDrop)
        input_box.move(coordx, coordy)
        input_box.setAcceptDrops(True)
        input_box.setStyleSheet("background-color: " + color + ";")
        return input_box

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

    def updateButtonsOnTime(self, milisecs):
        self._status_update_timer = QTimer(self)
        self._status_update_timer.setSingleShot(False)
        self._status_update_timer.timeout.connect(self.is_meshing_complete)
        self._status_update_timer.timeout.connect(self.is_simulation_complete)
        self._status_update_timer.start(500)


class QPushStopButton(QPushButton):
    def __init__(self, parent, move_x, move_y):
        super().__init__(parent)
        self.setIcon(QIcon('stop.png'))
        self.setIconSize(QtCore.QSize(parent.vis_stopButtonWidth, parent.vis_stopButtonWidth))
        self.move(move_x, move_y)

class QLineEditWithInputValue(QLineEdit):
    def __init__(self, parent, xcoord, ycoord, display_text, prefilltext):
        parent.display_text(parent, display_text, xcoord, ycoord, MediumFont, MediumFontSize)
        super().__init__(parent)
        self.move(xcoord + parent.vis_meshInputGap, ycoord-parent.vis_move_input_box_negative)
        self.resize(parent.vis_input_box_width, parent.vis_input_box_height)
        self.setText(str(prefilltext))
        self.setFont(QFont(MediumFont, MediumFontSize))
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)




class QPushButtonWithExtraFeatures(QPushButton):
    def __init__(self, parent, textToDisp, toolTipText, resize_width, resize_height, move_x, move_y):
        super().__init__(textToDisp, parent)
        self.setToolTip(toolTipText)
        self.resize(resize_width, resize_height)
        self.move(move_x, move_y)

class QLineEditWithDrop(QLineEdit):
    def __init__(self, title, parent, boxNumber, file_name, textToPrint,  fontStyle, fontSize):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.setReadOnly(True)
        self.boxNumber = boxNumber
        self.file_name = file_name
        self.parent = parent
        self.setText(textToPrint)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.setFont(QFont(fontStyle, fontSize))
        self.setStyleSheet("border: 1px dashed black;")

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
           e.accept()
           #print(e.mimeData.urls())

        else:
           e.ignore()

    def dropEvent(self, e):
        location1 = str(e.mimeData().urls())
        location = location1[20:-3]
        self.fileChecker(location)


    def fileChecker(self, locationFull):
        if locationFull[-3:] == 'x_t':
            #self.setText(locationFull)
            print(geometry_directory+self.change_to_file_name(self.boxNumber))
            if not locationFull[7:] == geometry_directory +self.change_to_file_name(self.boxNumber):
                copyfile(locationFull[7:], geometry_directory +self.change_to_file_name(self.boxNumber))
            else:
                pass
                #TODO: In status bar say location was the same
                #TODO: Create CFD/Input_Files directory

            print('It is a ' + self.change_to_file_name(self.boxNumber) + ' Box number:'+ str(self.boxNumber))
            self.parent.on_geo_check_click()
            #self.parent.geometryCheckModule()


        else:
            pass
            #TODO: In status bar say that it is not a parasolid file
            #TODO: If the refinement box is second then send to refinement box

    def change_to_file_name(self, number):
        if number == 1:
            return car_file_name
        if number == 2:
            return refbox_file_name
        if number == 3:
            return bndbox_file_name

if __name__== '__main__':
    app = QApplication(sys.argv)
    ex = App()
    #QtCore.QTimer.singleShot(2500, ex.close)
    sys.exit(app.exec_())
