#         #### exec(f'{system}_{state}_defect_site_x = {...}') # if defect is vacancy, write x-coordinate of removed atom
#         #### exec(f'{system}_{state}_defect_site_y = {...}') # if defect is vacancy, write y-coordinate of removed atom
#         #### exec(f'{system}_{state}_defect_site_z = {...}') # if defect is vacancy, write z-coordinate of removed atom
#         for d in 'x', 'y', 'z': #!*!
#             exec(f'{system}_{state}_diff_{d} = perf_{perfect_project_name}_{...}_{d} - {system}_{state}_{d}') # if
#             # state changed for perfect structure above to stop any iteration errors write what state was changed to
#             # in {...}
#             exec(f'{system}_{state}_defect_site_{d} = {system}_{state}_{d}[{...}]') # if defect is a substitional or
#             # interstitial defect, write atom index of subsituted/inserted atom. If defect is a vacancy comment
#             # out line and uncomment out the three lines prior to the for loop of d.
#             exec(f'{system}_{state}_distance_{d} = {system}_{state}_defect_site_{d} - {system}_{state}_{d}')
#         exec(f'{system}_{state}_tot_displacement = np.sqrt({system}_{state}_diff_x**2 + {system}_{state}_diff_y**2 +
#         {system}_{state}_diff_z**2)') ## vector magnitude of displacement from perfect structure geometry
#         exec(f'{system}_{state}_tot_distance = np.sqrt({system}_{state}_distance_x**2 + {system}_{state}_distance_y**2
#         + {system}_{state}_distance_z**2)') ## vector magnitude of distance from defect site
#         exec(f'{system}_{state}_tot_distance_sorted = np.sort({system}_{state}_tot_distance)') #!*! ## distances from
#         ## defect site sorted from smallest to largest
#         exec(f'{system}_{state}_tot_displacement_sorted = [x for _, x in sorted(zip({system}_{state}_tot_distance,
#         {system}_{state}_tot_displacement))]') ## displacements from perfect structure geometry sorted based
#                                                                                                                                                          #### on distance from defect site from smallest to largest
#         exec(f'{system}_{state}_tot_displacement_sorted2 = np.sort({system}_{state}_tot_displacement)') ## displacements
#         ## from perfect structure geometry sorted from smallest to largest

class SubstitutionalGeometry:
    def __init__(self, atom_index):
        e = 5
        print(e)

class InterstitionalGeometry:
    def __init__(self, atom_index):
        e = 11
        print(e)

class VacancyGeometry:
    def __init__(self, atom_index):
        e = 17
        print(e)

class SubsVacancyGeometry:
    def __init__(self, atom_index):
        e = 8
        print(e)

class InterVacancyGeometry:
    def __init__(self, atom_index):
        e = 9
        print(e)