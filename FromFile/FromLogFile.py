import FromFile

class GetChargesSpins:
    pop1 = 'Mulliken Population Analysis'
    pop2 = 'Hirshfeld Charges'
    def __init__(self, logfile, atomindex):
        self.index = atomindex
        self.pop1 = ''
        self.pop2 = ''
        log = open(logfile, 'r')
        lines = log.readlines()
        index = len(lines)
        for line in reversed(lines):
            if FromFile.GetChargesSpins.pop1 in line:
                PopAnalysisStart = index
                self.pop1 = PopAnalysisStart + int(self.index) + 1
            if FromFile.GetChargesSpins.pop2 in line:
                PopAnalysisStart = index
                self.pop2 = PopAnalysisStart + int(self.index) + 1
            index -=1
        log.close()
        log = open(logfile, 'r')
        for position, line in enumerate(log):
            if position == self.pop1:
                pop1_arr= line.split()
            if position == self.pop2:
                pop2_arr = line.split()
        log.close()
        self.pop1_charge = pop1_arr[5]
        self.pop1_spin = pop1_arr[6]
        self.pop1_beta_pop = pop1_arr[4]
        self.pop1_alpha_pop = pop1_arr[3]

        self.pop2_charge = pop2_arr[7]
        self.pop2_spin = pop2_arr[6]
        self.pop2_beta_pop = pop2_arr[5]
        self.pop2_alpha_pop = pop2_arr[4]

        self.returnchargespins()

    def returnchargespins(self):
        return self.pop1_charge, self.pop1_spin, self.pop1_alpha_pop, self.pop1_beta_pop, self.pop2_charge, self.pop2_spin, self.pop2_alpha_pop, self.pop2_beta_pop


#### ------------------------------------------------------------------------------------------------------ ####


# exec(f'{system}_{state}_energy_line = []')
# exec(f'{system}_{state}_gap_line = []')
# exec(f'{system}_{state}_gap= []')
# exec(f'{system}_{state}_energy = []')

# # -------------------------------------- LOG
# logfile = str("{}{}{}".format(output_file_hierarchy_directory, file, logname))
# log = open(logfile, 'r')  ## open file name saved as logfile
# index = 0
# for line in log:  ## iterate over every line in file
#     index += 1
#     if energy in line:  ## if the string called energy is found within a line
#         exec(
#             f'{system}_{state}_energy_index = index - 1')  ## first line is treated as line0 so number of line found containing string must be adjusted
#         exec(
#             f'{system}_{state}_energy_line.append({system}_{state}_energy_index)')  ## the line number of every line in which string is found is appended into an array
#     if gap in line:
#         exec(f'{system}_{state}_gap_index = index - 1')
#         exec(f'{system}_{state}_gap_line.append({system}_{state}_gap_index)')


# for item in 'energy', 'gap':
#     read_lines = eval("{}_{}_{}_line".format(system, state,
#                                              item))  ## read_lines needs to be define for each item so that the following for loop can be carried out automatically
#     log = open(logfile, 'r')  ## log file must be reasigned
#     for position, line in enumerate(
#             log):  ## enumerate used to search file and return the text string found on line numbers specified by position
#         if position in read_lines:
#             strg = line
#             exec(
#                 f'arr_{system}_{state}_{item} = strg.split()')  ## split text string of line into individual string based on column grouping of line
#             exec(
#                 f'arr_{system}_{state}_{item} = float(arr_{system}_{state}_{item}[-1])')  ## record line's last column string value as a float
#             exec(
#                 f'{system}_{state}_{item}.append(arr_{system}_{state}_{item})')  ## append each line's last column float value within an array
#     log.close()
#
# exec(
#     f'E_{system}_{state} = {system}_{state}_energy[-1] * 27.211')  ## To get final energy of calculation and convert it from hartree units into eV
# exec(
#     f'alpha_HOMO_LUMOgap_{system}_{state} = {system}_{state}_gap[-2]')  ## Second to last array entry is the seperation in energy (eV) between HOMO and LUMO of alpha spin state
# exec(
#     f'beta_HOMO_LUMOgap_{system}_{state} = {system}_{state}_gap[-1]')  ## Last array entry is the seperation in energy (eV) between HOMO and LUMO of beta spin state

