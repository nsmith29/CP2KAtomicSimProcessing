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
        else:
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
        subsubdirs = []
        var_suffix = []
        paths = [wd]
        for path in paths:
            dwd = str(self.cwd + "/" + path)
            obj = os.scandir(dwd)
            for entry in obj:
                if not entry.name.startswith('.') and entry.is_dir():
                    if Core.UserArguments.Exception is False:
                        paths.append(os.path.join(path, str("{}".format(entry.name))))
                    elif Core.UserArguments.Exception is True:
                        if type(Core.UserArguments.NotDir) == list:
                            if all(elem not in entry.name for elem in Core.UserArguments.NotDir):
                                paths.append(os.path.join(path, str("{}".format(entry.name))))
                            else:
                                if entry.name.find(Core.UserArguments.NotDir) == -1:
                                    paths.append(os.path.join(path, str("{}".format(entry.name))))
                elif not entry.name.startswith('.') and entry.is_file():
                    if Core.UserArguments.Only is True:
                        if type(Core.UserArguments.OnlyDir) == list:
                            if any(elem in path for elem in Core.UserArguments.OnlyDir):
                                if entry.name.endswith(file_extension):
                                    subsubdirs.append(dwd)
                                    var_suffix.append(path.replace('/', '_'))
                        else:
                            if path.find(Core.UserArguments.OnlyDir) != -1:
                                if entry.name.endswith(file_extension):
                                    subsubdirs.append(dwd)
                                    var_suffix.append(path.replace('/', '_'))
                    elif Core.UserArguments.Only is False:
                        if entry.name.endswith(file_extension):
                            subsubdirs.append(dwd)
                            var_suffix.append(path.replace('/', '_'))
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
