import os

screen_fraction = 2

car_file_name = 'car.x_t'
refbox_file_name = 'refbox.x_t'
bndbox_file_name = 'bndbox.x_t'

current_file_dir = os.path.dirname(os.path.abspath(__file__))


greyColor = '#ACA09D'
greenColor = '#90EE90'
redColor = '#DF7F67'

#Set Numeca paths
hybridPath = "/common/numeca/bin/hexpresshybridopen72"
FOpath = "/common/numeca/bin/fineopen72"


geometry_directory =     current_file_dir = os.path.dirname(os.path.abspath(__file__))+'/CFD/Input_Files/'
meshing_directory =  current_file_dir = os.path.dirname(os.path.abspath(__file__))+'/CFD/Mesh_Gen/'
conf_file_location = meshing_directory + 'mesh.conf'
simulation_directory = current_file_dir = os.path.dirname(os.path.abspath(__file__))+'/CFD/Simulation/'
simulationMacro = simulation_directory+'FOmacro.py'
projectName = "mySimulation"
meshName = "mesh.hex"
simulationBat = simulation_directory+projectName+'/'+projectName+'_computation_1/'+projectName+'_computation_1.batch'



LargeFont = 'Arial'
LargeFontSize = 30/screen_fraction

MediumFont ='Arial'
MediumFontSize = 20/screen_fraction



