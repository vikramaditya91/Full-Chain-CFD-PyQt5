import os

display_fraction_of_screen = 1.1

car_file_name = 'car.x_t'
refbox_file_name = 'refbox.x_t'
bndbox_file_name = 'bndbox.x_t'

current_file_dir = os.path.dirname(os.path.abspath(__file__))

input_geometry_destination = current_file_dir+'/CFD/Input_Files'

greyColor = '#ACA09D'
greenColor = '#90EE90'
redColor = '#DF7F67'

#Set Numeca paths
hybridPath = "/common/numeca/bin/hexpresshybridopen72"
FOpath = "/common/numeca/bin/fineopen72"




one_third_x = 1920 * 1 / 3
two_third_x = 1920 * 2 / 3
full_x = 1920

one_third_y = 1024 * 1 / 3
two_third_y = 1024 * 2 / 4
full_y = 1024

LargeFont = 'Arial'
LargeFontSize = 30

MediumFont ='Arial'
MediumFontSize = 20

widthBox = 50
heightBox = 50


carBoxx = 400
carBoxy = 600

refBoxx = 400
refBoxy = 700

bndBoxx = 400
bndBoxy = 800


#Meshing locations
first_cell_x = 615
first_cell_y = 500

second_cell_x = 615
second_cell_y = 575

third_cell_x = 615
third_cell_y = 650

fourth_cell_x = 615
fourth_cell_y = 725
