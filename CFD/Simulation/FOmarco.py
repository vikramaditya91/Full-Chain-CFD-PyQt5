script_version(2.2)
FHX.create_project("mySimulation")
FHX.set_active_computations([0])
FHX.link_mesh_file("../Mesh-Gen/mesh.igg")
FHX.set_precision_mode("double")
FHX.set_mathematical_model(0, K_OMEGA_M_SST_EXT_WALL_FUNCTION)
FHX.set_preconditioning(0, 1)
FHX.set_preconditioning(0, 1)
FHX.set_preconditioning(0, 1)
FHX.set_preconditioning(0, 1)
FHX.get_bc_patch(0, 7).set_parameter_value("Vy", 5)
FHX.get_bc_patch(0, 7).set_parameter_value("k", 2.78e-05)
FHX.get_bc_patch(0, 7).set_parameter_value("Epsilon", 4.63e-06)
FHX.get_bc_patch(0, 0).set_compute_force_and_torque_flag(1)
FHX.get_bc_patch(0, 1).set_compute_force_and_torque_flag(1)
FHX.get_bc_patch(0, 2).set_compute_force_and_torque_flag(1)
FHX.get_bc_patch(0, 3).set_compute_force_and_torque_flag(1)
FHX.get_bc_patch(0, 4).set_compute_force_and_torque_flag(1)
FHX.get_initial_solution(0).set_velocity(Vector(0,25, 0))
FHX.get_initial_solution(0).set_k_epsilon(2.78e-05, 4.6299999999999995e-07)
FHX.set_CPU_booster_flag(1)
FHX.set_MG_level_number(3)
FHX.set_MG_number_of_cycles(500)
FHX.set_MG_CPU_booster_flag(0)
FHX.set_MG_CFL_number(1)
FHX.set_numerical_scheme(0, CENTRAL_MATRIX_SCHEME)
FHX.set_preconditioning_method(0, MERKLE)
FHX.set_preconditioning_characteristic_velocity(0, 25)
FHX.set_outputs_flow_configuration(0, 0)
FHX.set_outputs_reference_flag(0, 1)
FHX.set_convergence_criteria(-10)
FHX.set_nb_iter_max(1000)
FHX.set_launching_mode(1)
FHX.set_number_of_processes(4)
FHX.save_project()
FHX.save_selected_computations()
FHX.save_batch_file()