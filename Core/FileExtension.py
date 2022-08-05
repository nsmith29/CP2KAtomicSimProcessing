import os
import Core

class Extension:
    def __init__(self):
        self.cwd = os.getcwd()

    def current_work_directory(self):
        return self.cwd
        # self.perfect_subdir()

    def perfect_subdir(self, file_extension, wd):
        # want to find inp, log, pdos, xyz
        if file_extension == ".pdos":
            files = []
        elif file_extension == ".inp":
            File = ' '
        perfwd = str(self.cwd + "/" + wd)
        for file in os.listdir(perfwd):
            if os.path.isfile(os.path.join(perfwd, file)) and file.endswith(file_extension):
                File = os.path.join(perfwd, file)
                if file_extension == ".pdos":
                    files.append(File)

        if file_extension == ".inp":
            File = self.check_input_file_available(perfwd, File)
        if file_extension == ".pdos":
            return files
        else:
            return File

    def All_defect_subdir(self, file_extension, wd):
        # want to take note of all subdirectories until inp, log, pdos, xyz files found
        dwd = str(self.cwd + "/" + wd)
        def_subdir = wd
        subsubdirs = []
        var_suffix = []
#glob or os file io-
        for sub1item in os.listdir(dwd): # 1st tier
            if os.path.isdir(os.path.join(dwd, sub1item)): # tier 1 opt 1
                for sub2item in os.listdir(os.path.join(dwd, sub1item)): # 2nd tier
                    if os.path.isdir(os.path.join(dwd, sub1item, sub2item)): # tier 2 opt 1
                        for sub3item in os.listdir(os.path.join(dwd, sub1item, sub2item)): # 3rd tier
                            if sub3item != ".ipynb_checkpoints":
                                if os.path.isdir(os.path.join(dwd, sub1item, sub2item, sub3item)): # tier 3 opt 1
                                    for sub4item in os.listdir(os.path.join(dwd, sub1item, sub2item, sub3item)): # 4th tier
                                        if os.path.isdir(os.path.join(dwd, sub1item, sub2item, sub3item, sub4item)): # tier 4 opt 1
                                            for sub5item in os.listdir(os.path.join(dwd, sub1item, sub2item, sub3item, sub4item)): # 5th tier
                                                if os.path.isdir(os.path.join(dwd, sub1item, sub2item, sub3item, sub4item, sub5item)): # tier 5 opt 1
                                                    for sub6item in os.listdir(os.path.join(dwd, sub1item, sub2item, sub3item, sub4item, sub5item)):
                                                        if os.path.isfile(os.path.join(dwd, sub1item, sub2item, sub3item, sub4item, sub5item, sub6item)):
                                                            if sub6item.endswith(file_extension):
                                                                print('hi, you need to add another for-if cycle')
                                                if os.path.isfile(os.path.join(dwd, sub1item, sub2item, sub3item, sub4item, sub5item)): # tier 5 opt 2
                                                    if sub5item.endswith(file_extension):
                                                        sub_dir_path = os.path.join(dwd, sub1item, sub2item, sub3item, sub4item)
                                                        subsubdirs.append(sub_dir_path)
                                                        name = str(def_subdir + "_" + sub1item + "_" + sub2item + "_" + sub3item + "_"+ sub4item)
                                                        var_suffix.append(name)
                                        if os.path.isfile(os.path.join(dwd, sub1item, sub2item, sub3item, sub4item)): # tier 4 opt 2
                                            if sub4item.endswith(file_extension):
                                                sub_dir_path = os.path.join(dwd, sub1item, sub2item, sub3item)
                                                subsubdirs.append(sub_dir_path)
                                                name = str(def_subdir + "_" + sub1item + "_" + sub2item + "_" + sub3item)
                                                var_suffix.append(name)
                                elif os.path.isfile(os.path.join(dwd, sub1item, sub2item, sub3item)): # tier 3 opt 2
                                    if sub3item.endswith(file_extension):
                                        sub_dir_path = os.path.join(dwd, sub1item, sub2item)
                                        subsubdirs.append(sub_dir_path)
                                        name = str(def_subdir + "_" + sub1item + "_" + sub2item)
                                        var_suffix.append(name)
                    elif os.path.isfile(os.path.join(dwd, sub1item, sub2item)): # tier 2 opt 2
                        if sub2item.endswith(file_extension):
                            sub_dir_path = os.path.join(dwd, sub1item)
                            subsubdirs.append(sub_dir_path)
                            name = str(def_subdir + "_" + sub1item)
                            var_suffix.append(name)
            elif os.path.isfile(os.path.join(dwd, sub1item)): # tier 1 opt 2
                if sub1item.endswith(file_extension):
                    sub_dir_path = os.path.join(dwd)
                    subsubdirs.append(sub_dir_path)
                    name = str(def_subdir)
                    var_suffix.append(name)

        if Core.UserArguments.Exception is True:
            if type(Core.UserArguments.NotDir) == list:
                for elem in list(Core.UserArguments.NotDir):
                    for elem1, elem2 in zip(list(subsubdirs), list(var_suffix)):
                        if elem1.find(elem) != -1:
                            subsubdirs.remove(elem1)
                            var_suffix.remove(elem2)
            else:
                for elem1, elem2 in zip(list(subsubdirs), list(var_suffix)):
                    if elem1.find(Core.UserArguments.NotDir) != -1:
                        subsubdirs.remove(elem1)
                        var_suffix.remove(elem2)

        if Core.UserArguments.Only is True:
            changedirs = []
            changesufs = []
            if type(Core.UserArguments.OnlyDir) == list:
                for elem in list(Core.UserArguments.OnlyDir):
                    for elem1, elem2 in zip(list(subsubdirs), list(var_suffix)):
                        elem3 = str(elem1 + "/")
                        if elem3.find(elem) != -1:
                            dir = elem1
                            suf = elem2
                            changedirs.append(dir)
                            changesufs.append(suf)

            else:
                for elem1, elem2 in zip(list(subsubdirs), list(var_suffix)):
                    elem3 = str(elem1 + "/")
                    if elem3.find(Core.UserArguments.OnlyDir) != -1:
                        dir = elem1
                        sur = elem2
                        changedirs.append(dir)
                        changesufs.append(sur)
            subsubdirs = changedirs
            var_suffix = changesufs

        return subsubdirs, var_suffix

    def files4defect(self, file_extension, subdir):
        global files
        if file_extension == ".pdos":
            files = []
        if file_extension == ".inp":
            File = " "
        for file in os.listdir(subdir):
            if os.path.isfile(os.path.join(subdir, file)):
                if file.endswith(file_extension):
                    File = os.path.join(subdir, file)
                    if file_extension == ".pdos":
                        files.append(File)
                    else:
                        files = File
        if file_extension == ".inp":
            self.check_input_file_available(subdir, files)

        return files

    def check_input_file_available(self, wd, input_file):
        for file in os.listdir(wd):
            if input_file == ' ':
                if os.path.isfile(os.path.join(wd, file)):
                    if file.endswith(".restart"):
                        inp_file = os.path.join(wd, file)
                        return inp_file
            else:
                return input_file


Extension()
