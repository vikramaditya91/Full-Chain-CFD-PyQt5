import os
from variables import *


def color_return(parasolid_file):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    file_exists = os.path.exists(current_file_dir + '/CFD/Input_Files/' + parasolid_file)

    if file_exists:
        return greenColor

    if not file_exists:
        return redColor


def generateConfFile(baseH, refCarRefinement, refBoxRefinement):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    # TODO: Create Mesh_Gen if not already available
    conf_location = current_file_dir + '/CFD/Mesh_Gen/mesh.conf'

    try:
        os.remove(conf_location)
    except OSError:
        pass

    with open(conf_location, 'a+') as f:
        f.write('INFILENAMES 2\n')
        f.write('../Input_Files/' + car_file_name + '\n')
        f.write('../Input_Files/' + bndbox_file_name + '\n\n')

        f.write('ADDINFILENAMES 1' + '\n')
        f.write('../Input_Files/' + refbox_file_name + '\n\n')

        f.write('OUTFILENAME mesh.hex' + '\n\n')
        f.write('USEBINFILEVERSION 11' + '\n')
        f.write('BASEH ' + baseH + '\n')
        f.write('MARKBYSTARTPOINT 80 10 10' + '\n')
        f.write('CREATESELECTIONSBYANGLE ALLEDGES SPLIT edge 40 1 *' + '\n')

        f.write(
            'LOCALREFINEMENTDEFINITION ' + car_file_name[:-4] + '* ' + refCarRefinement + ' ' + refCarRefinement + '\n')
        f.write('ADDLOCALREFINEMENTDEFINITION ' + refbox_file_name[
                                                  :-4] + '* ' + refBoxRefinement + ' ' + refBoxRefinement + ' 1' + '\n\n')
        f.write('BCDEFINITION * SOL' + '\n')

        f.write('END')

    return conf_location


def generateSimulationMacro(inletVel, turbIntensity, liftDir, dragDir):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    # TODO: to create a folder Simulation if not alreayd present
    FOmacro = current_file_dir + '/CFD/Simulation/FOmarco.py'


    #TODO: Clean up inletVel


    if dragDir == 'X':
        inletVelocity = 'Vx'
        initVelVector = inletVel + ',0, 0'
    elif dragDir == 'Y':
        inletVelocity = 'Vy'
        initVelVector = '0,' +inletVel+ ', 0'
    elif dragDir == 'Z':
        inletVelocity = 'Vz'
        initVelVector = '0, 0,'+inletVel

    k = calc_TKE_from_intensity(turbIntensity)
    epsilon = calc_epsilon_from_TKE(k)

    #TODO: Format checks for inlet values

    try:
        os.remove(FOmacro)
    except OSError:
        pass

    #TODO: Getting correct bcs from bcs file? and their numbers

    with open(FOmacro, 'a+') as f:
        f.write('script_version(2.2)\n')
        f.write('FHX.create_project("mySimulation")\n')
        f.write('FHX.set_active_computations([0])\n')
        f.write('FHX.link_mesh_file("../Mesh-Gen/mesh.igg")'+ '\n')
        f.write('FHX.set_precision_mode("double")'+ '\n')
        f.write('FHX.set_mathematical_model(0, K_OMEGA_M_SST_EXT_WALL_FUNCTION)'+ '\n')
        f.write('FHX.set_preconditioning(0, 1)'+ '\n')

        f.write('FHX.set_preconditioning(0, 1)'+ '\n')
        f.write('FHX.set_preconditioning(0, 1)'+ '\n')
        f.write('FHX.set_preconditioning(0, 1)'+ '\n')
        f.write('FHX.get_bc_patch(0, 7).set_parameter_value("' + str(inletVelocity) + '", 5)'+ '\n')
        f.write('FHX.get_bc_patch(0, 7).set_parameter_value("k", '+ str(k) + ')'+ '\n')
        f.write('FHX.get_bc_patch(0, 7).set_parameter_value("Epsilon", '+ str(epsilon) +')'+ '\n')

        f.write('FHX.get_bc_patch(0, 0).set_compute_force_and_torque_flag(1)'+ '\n')
        f.write('FHX.get_bc_patch(0, 1).set_compute_force_and_torque_flag(1)'+ '\n')
        f.write('FHX.get_bc_patch(0, 2).set_compute_force_and_torque_flag(1)'+ '\n')
        f.write('FHX.get_bc_patch(0, 3).set_compute_force_and_torque_flag(1)'+ '\n')
        f.write('FHX.get_bc_patch(0, 4).set_compute_force_and_torque_flag(1)'+ '\n')

        f.write('FHX.get_initial_solution(0).set_velocity(Vector('+ initVelVector+'))'+ '\n')
        f.write('FHX.get_initial_solution(0).set_k_epsilon('+str(k)+', '+str(epsilon/10)+')'+ '\n')

        f.write('FHX.set_CPU_booster_flag(1)'+ '\n')
        f.write('FHX.set_MG_level_number(3)'+ '\n')
        f.write('FHX.set_MG_number_of_cycles(500)'+ '\n')
        f.write('FHX.set_MG_CPU_booster_flag(0)'+ '\n')
        f.write('FHX.set_MG_CFL_number(1)'+ '\n')
        f.write('FHX.set_numerical_scheme(0, CENTRAL_MATRIX_SCHEME)'+ '\n')
        f.write('FHX.set_preconditioning_method(0, MERKLE)'+ '\n')

        f.write('FHX.set_preconditioning_characteristic_velocity(0, '+inletVel+')'+ '\n')
        f.write('FHX.set_outputs_flow_configuration(0, 0)'+ '\n')
        f.write('FHX.set_outputs_reference_flag(0, 1)'+ '\n')
        f.write('FHX.set_convergence_criteria(-10)'+ '\n')
        f.write('FHX.set_nb_iter_max(1000)'+ '\n')

        f.write('FHX.set_launching_mode(1)'+ '\n')
        f.write('FHX.set_number_of_processes(4)'+ '\n')
        f.write('FHX.save_project()'+ '\n')
        f.write('FHX.save_selected_computations()'+ '\n')
        f.write('FHX.save_batch_file()'+ '\n')

        #TODO Set directions for drag and lift

        return FOmacro

def calc_TKE_from_intensity(TI):
    return 2.78E-05

def calc_epsilon_from_TKE(TKE):
    return 4.63E-6



