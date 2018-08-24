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

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.screenAdjust ()
        self.allText()
        self.title = 'Full chain CFD'
        self.allGeometriesPresent = False
        self.meshReady = False
        self.carColor = redColor
        self.refBoxColor = redColor
        self.bndBoxColor = redColor
        self.geometryCheckModule()
        self.meshingModule()
        self.simulationModule()
        self.initUI()
        self.setAcceptDrops(True)
        self.update()
        self.movie = QMovie("loading.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.meshRunning = False

        self._status_update_timer = QTimer(self)
        self._status_update_timer.setSingleShot(False)
        self._status_update_timer.timeout.connect(self.is_meshing_complete)
        self._status_update_timer.start(500)

    def screenAdjust (self):
        self.screen_size = QDesktopWidget().screenGeometry()
        self.resize(self.screen_size.width() / display_fraction_of_screen, self.screen_size.height() / display_fraction_of_screen)

        self.GUIsize = self.geometry()

        self.move((self.screen_size.width() - self.GUIsize.width()) / 2,
                      (self.screen_size.height() - self.GUIsize.height()) / 2)

        ##WIDTH
        self.vis_one_third_x = self.GUIsize.width() / 3
        self.vis_two_third_x = self.GUIsize.width() * 2 / 3
        self.vis_half_x = self.GUIsize.width() / 2
        self.vis_full_x = self.GUIsize.width()
        self.vis_before_title1_x = self.vis_one_third_x/5

        self.vis_firstColumn1 = self.vis_one_third_x / 2.25
        self.vis_geoName_locs = self.vis_one_third_x/6

        self.vis_geometry_button_x = self.vis_one_third_x/4.5
        self.vis_mesh_button_x  = self.vis_full_x/2.5

        self.vis_before_title2_x = self.vis_full_x/2.5
        self.vis_meshName_locs = self.vis_full_x/2.5
        self.vis_pushButtonWidth = self.vis_full_x/5.5

        ##HEIGHT
        self.vis_one_third_y = self.GUIsize.height() / 3
        self.vis_two_third_y = self.GUIsize.height() * 2 / 3
        self.vis_half_y = self.GUIsize.height() / 2
        self.vis_full_y = self.GUIsize.height()

        self.vis_geo_heightLevel1 = self.GUIsize.height() * 0.6
        self.vis_geo_heightLevel2 = self.GUIsize.height() * 0.725
        self.vis_geo_heightLevel3 = self.GUIsize.height() * 0.85

        self.vis_geometry_button_y = self.vis_two_third_y*1.425
        self.vis_mesh_heightLevel1 = self.GUIsize.height() * 0.6
        self.vis_mesh_heightLevel2 = self.GUIsize.height() * 0.7
        self.vis_mesh_heightLevel3 = self.GUIsize.height() * 0.8
        self.vis_mesh_heightLevel4 = self.GUIsize.height() * 0.9

        self.vis_pushButtonHeight = self.vis_full_y/15

        self.vis_widthBoxDrop = self.vis_one_third_x / 1.5
        self.vis_heightBoxDrop = self.vis_one_third_y / 6

        self.vis_image_move_x = self.vis_one_third_x/1.5
        self.vis_image_move_y = self.vis_one_third_x/4

    def allText(self):
        self.text_geometryTitle = 'Check Geometry  '
        self.test_carName = 'Car'
        self.text_refinementBoxName = 'Refinement box'
        self.text_boundingBoxName = 'Bounding box'
        self.text_geometryCheckButton = 'Check if geometries exist'
        self.text_geometryCheckButtonTooltip = 'Searches Input_Files \
        directory for \n Parasolid files of car, \nrefinement box, bounding box'

        self.text_meshTitle = 'Mesh Setup '
        self.text_meshStartButtonText = 'Start mesh generation'
        self.text_meshStartButtontooltip = 'This starts the mesh generation process'

        self.simulationTitle = 'Simulation Setup  '

        self.text_Bad = u'\u2717'
        self.text_Good = u'\u2713'

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
        #currentFrame = self.movie.currentPixmap()
        #frameRect = currentFrame.rect()
        #frameRect.moveCenter(self.rect().center())
        #if frameRect.intersects(e.rect()):# and self.meshRunning == True:
        #    painter = QPainter(self)
        #    painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

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

        self.carText = self.display_textWithDrop(self, self.test_carName ,
                                                   self.vis_geoName_locs,
                                                   self.vis_geo_heightLevel1, MediumFont, MediumFontSize)

        #self.carInput = self.draw_input_box(self.vis_geoName_locs, self.vis_geo_heightLevel1, 1, car_file_name, self.test_carName, self.carColor)
        self.refBoxInput = self.draw_input_box(self.vis_geoName_locs, self.vis_geo_heightLevel2, 2, refbox_file_name, self.text_refinementBoxName, self.refBoxColor)
        self.bndBoxInput = self.draw_input_box(self.vis_geoName_locs, self.vis_geo_heightLevel3, 3, bndbox_file_name, self.text_boundingBoxName, self.bndBoxColor)

        # Check geometry button
        self.QPushButtonWithExtraFeatures(self, self.text_geometryCheckButton , self.text_geometryCheckButtonTooltip ,
                                          self.vis_pushButtonWidth, self.vis_pushButtonHeight, self.vis_geometry_button_x , self.vis_geometry_button_y  ).clicked.connect(self.on_geo_check_click)

        self.update()

    @pyqtSlot()
    def on_geo_check_click(self):

        self.carInput.setStyleSheet("background-color: "+color_return(car_file_name)+";")
        self.refBoxInput.setStyleSheet("background-color: " + color_return(refbox_file_name) + ";")
        self.bndBoxInput.setStyleSheet("background-color: " + color_return(bndbox_file_name) + ";")

        #self.carInput.
        print('In geometry check click')
        if color_return(car_file_name) == greenColor and color_return(refbox_file_name) == greenColor and color_return(bndbox_file_name) == greenColor:
            self.allGeometriesPresent = True
            self.geometryCheckText.setText(self.text_geometryTitle + self.text_Good)
            self.meshButton.setEnabled(True)
            #TODO: Do not fully understand

    def meshingModule(self):
        # Meshing setup
        self.meshCheckText = self.display_text(self, self.text_geometryTitle + self.text_Bad, self.vis_before_title2_x,
                                                   self.vis_half_y, LargeFont, LargeFontSize)


        self.BaseHText = self.QLineEditWithExtraFeatures(self, self.vis_meshName_locs, self.vis_mesh_heightLevel1, 'Cell Size in Domain', 0.5)
        self.refCarText = self.QLineEditWithExtraFeatures(self, self.vis_meshName_locs, self.vis_mesh_heightLevel2, 'Refinements on car', 5)
        self.refBoxText = self.QLineEditWithExtraFeatures(self, self.vis_meshName_locs, self.vis_mesh_heightLevel3,'Refinements on \nrefinement box', 3)


        self.meshButton = self.QPushButtonWithExtraFeatures(self, self.text_meshStartButtonText , self.text_meshStartButtontooltip ,
                                          self.vis_pushButtonWidth, self.vis_pushButtonHeight, self.vis_mesh_button_x , self.vis_geometry_button_y  )\

        self.meshButton.clicked.connect(self.on_mesh_generation_click)

        if self.allGeometriesPresent == False:
            self.meshButton.setEnabled(False)

    @pyqtSlot()
    def on_mesh_generation_click(self):
        baseH = self.BaseHText.text()
        refCarRefinement = self.refCarText.text()
        refBoxRefinement = self.refBoxText.text()

        confLocation  = generateConfFile(baseH, refCarRefinement, refBoxRefinement)
        print(hybridPath + " "+confLocation)
        os.system(hybridPath + " "+confLocation +" -print")
        self.meshRunning = True
        self.is_meshing_complete()

        self.movie.start()
        #check_output(hybridPath + " "+confLocation, shell=True)


        #time.sleep(1)

    def is_meshing_complete(self):
        my_file = os.path.dirname(os.path.abspath(__file__)) + "/CFD/mesh.hex"
        if os.path.exists(my_file):
            self.simulationButton.setEnabled(True)
            self.movie.stop()
            self.meshRunning = False

    def simulationModule(self):
        self.simulationButton = self.QPushButtonWithExtraFeatures(self, 'Start simulation', 'Starts simulation', 300, 40, fourth_cell_x + 600,
                                          fourth_cell_y + 100)
        self.simulationButton.clicked.connect(self.on_simulation_button_click)


        self.display_text(self, 'Simulation Setup', (two_third_x) / 1.8+450, two_third_y / 1.25, LargeFont, LargeFontSize)

        self.inletVelText = self.QLineEditWithExtraFeatures(self, first_cell_x+500, first_cell_y, 'Inlet Velocity', 25)
        self.turbIntensityText = self.QLineEditWithExtraFeatures(self, second_cell_x+500, second_cell_y, 'Turbulence Intensity', '4%')
        self.liftDirText = self.QLineEditWithExtraFeatures(self, third_cell_x + 500, third_cell_y, 'Lift direction', 'X')
        self.dragDirText = self.QLineEditWithExtraFeatures(self, third_cell_x + 500, fourth_cell_y, 'Drag direction', 'Y')

        if self.meshReady == False:
            self.simulationButton.setEnabled(False)



    @pyqtSlot()
    def on_simulation_button_click(self):
        inletVelocity = self.inletVelText.text()
        turbulenceIntensity = self.turbIntensityText.text()
        liftDirection = self.liftDirText.text()
        dragDirection = self.dragDirText.text()

        pythonFOMacroLocation = generateSimulationMacro(inletVelocity, turbulenceIntensity, liftDirection, dragDirection)
        print(FOpath + " " + pythonFOMacroLocation)
        check_output(FOpath + " " + pythonFOMacroLocation, shell=True)

    def initUI(self):
        self.setWindowTitle(self.title)
        # Insert domain image
        label = QLabel(self)
        pixmap = QPixmap('GIMP_Domain.png')
        pixmap = pixmap.scaledToWidth(1000)
        label.setPixmap(pixmap)
        label.move(self.vis_image_move_x, self.vis_image_move_y)

        self.show()
        #self.showMaximized()
    def draw_input_box(self, coordx, coordy, boxNumber, file_name , nameToPrint, color):
            input_box = QLineEditWithDrop('', self, boxNumber, file_name, nameToPrint, MediumFont, MediumFontSize)
            input_box.setDragEnabled(True)
            input_box.resize(self.vis_widthBoxDrop, self.vis_heightBoxDrop)
            input_box.move(coordx, coordy)
            input_box.setAcceptDrops(True)
            input_box.setStyleSheet("background-color: "+color+";")
            return input_box

    def display_text(self, parent, toPrint, whereX, whereY, fontStyle, fontSize):
            disp_text = QLabel(parent)
            disp_text.setText(toPrint)
            disp_text.move(whereX, whereY)
            disp_text.setFont(QFont(fontStyle, fontSize))
            return disp_text

    class QLineEditWithExtraFeatures(QLineEdit):
        def __init__(self, parent , xcoord, ycoord, display_text, prefilltext):
            super().__init__(parent)
            self.move(xcoord+300, ycoord)
            self.resize(75, 30)
            self.setText(str(prefilltext))

            parent.display_text(parent, display_text, xcoord, ycoord, MediumFont, MediumFontSize )

    class QPushButtonWithExtraFeatures(QPushButton):
        def __init__(self, parent, textToDisp, toolTipText, resize_width, resize_height, move_x, move_y):
            super().__init__(textToDisp, parent)
            self.setToolTip(toolTipText)
            self.resize(resize_width, resize_height)
            self.move(move_x, move_y)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()


class QLineEditWithDrop(QLineEdit):
    def __init__(self, title, parent, boxNumber, file_name, textToPrint,  fontStyle, fontSize):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
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
            print(input_geometry_destination + '/'+self.change_to_file_name(self.boxNumber))
            if not locationFull[7:] == input_geometry_destination + '/'+self.change_to_file_name(self.boxNumber):
                copyfile(locationFull[7:], input_geometry_destination + '/'+self.change_to_file_name(self.boxNumber))
            else:
                pass
                #TODO: In status bar say location was the same
                #TODO: Create CFD/Input_Files directory

            print('It is a ' + self.change_to_file_name(self.boxNumber) + ' Box number:'+ str(self.boxNumber))
            self.parent.on_geo_check_click()
            self.parent.geometryCheckModule()


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

class QLineWithDrop(QLineEdit):
    def __init__(self, title, parent, boxNumber, file_name, textToPrint,  fontStyle, fontSize):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
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
            print(input_geometry_destination + '/'+self.change_to_file_name(self.boxNumber))
            if not locationFull[7:] == input_geometry_destination + '/'+self.change_to_file_name(self.boxNumber):
                copyfile(locationFull[7:], input_geometry_destination + '/'+self.change_to_file_name(self.boxNumber))
            else:
                pass
                #TODO: In status bar say location was the same
                #TODO: Create CFD/Input_Files directory

            print('It is a ' + self.change_to_file_name(self.boxNumber) + ' Box number:'+ str(self.boxNumber))
            self.parent.on_geo_check_click()
            self.parent.geometryCheckModule()


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
    #QtCore.QTimer.singleShot(5500, ex.close)
    sys.exit(app.exec_())
