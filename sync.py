import os
import subprocess
from enums import Path
import datetime

class Sync:
    
# START==================================================GlOBAL VARIABLES===================================================#

    curr_pc_os = ""

# END==================================================GlOBAL VARIABLES===================================================#

# START==================================================SYNC UTILS=========================================================#

    def __init__(self, android_path, pc_path):
        self.android_path = android_path
        self.pc_path = pc_path
    
    @staticmethod
    def is_valid_extension(extension):
        allowed_extensions = (".bak", ".plr", ".wld")
        if extension.lower() in allowed_extensions:
            return True
        return False

    @staticmethod
    def check_pc_os():
        if os.name == "posix":
            return Path.LINUX
        elif os.name == "nt":
            return Path.WINDOWS
        else:
            print("The PC operating system is not supported")
            return False

    @staticmethod
    def check_adb_connection():
        output = subprocess.check_output(["adb", "devices"]).decode()
        lines = output.strip().split('\n')
        if len(lines) > 1:
            devices = lines[1:]
            for device in devices:
                if "device" in device:
                    return True        
        print("Android device cannot be found through adb connection")
        return False

    def check_pc_dir(path):
        if os.path.exists(path):
            return True
        else:
            print("Terraria path on PC does not exist")
            return False
    
    def check_android_dir(path):
        command = ["adb", "shell", "ls",  path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Terraria path on android does not exist")
            print("Error:", error.decode())
            return False
        return True
    
    def get_second_to_last_word(path):
        slash_list = []
        for index, slash in enumerate(path):
            if slash == "\\" or slash == "/":
                slash_list.append(index)
        second_last_slash_index = slash_list[-2] if len(slash_list) >= 2 else -1
        return path[second_last_slash_index+1:max(slash_list)]

    @staticmethod
    def pull_files_from_android(path_list):
        for path in path_list:
            source_path = path
            if Sync.curr_pc_os == Path.WINDOWS:
                destination_path = os.path.join(Path.WINDOWS.get_terraria_rootpath(), Sync.get_second_to_last_word(source_path)).replace("\\", "/")
            elif Sync.curr_pc_os == Path.LINUX:
                destination_path = os.path.join(Path.WINDOWS.get_terraria_rootpath(), Sync.get_second_to_last_word(source_path)).replace("\\", "/")
            command = ["adb", "pull", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout, end="")
            if process.stderr:
                print("Error:", process.stderr, end="")
        
    @staticmethod
    def push_files_to_android(path_list):
        for path in path_list:
            source_path = path
            destination_path = os.path.join(Path.ANDROID.get_terraria_rootpath(), Sync.get_second_to_last_word(source_path)).replace("\\", "/")
            command = ["adb", "push", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout, end="")
            if process.stderr:
                print("Error:", process.stderr, end="")

# END==================================================SYNC UTILS=========================================================#
    
# START==================================================SYNC OPERATION====================================================#
    def execute_sync(self):
        '''Extracts the file paths and its last modified dates, placing it in a dictionary, then to a list.'''
        Sync.check_android_dir(self.android_path)
        Sync.check_pc_dir(self.pc_path)

        android_path_date_list = []
        command = ["adb", "shell", "ls", self.android_path]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if not Sync.is_valid_extension(extension):
                continue
            file_path =  os.path.join(self.android_path, file).replace("\\", "/")
            command = ["adb", "shell", "stat", "-c", "%y", file_path]
            process = subprocess.run(command, capture_output=True, text=True)
            output = process.stdout.strip()
            last_modified = datetime.datetime.strptime(output[:19], "%Y-%m-%d %H:%M:%S")
            last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")

            android_path_date_dict = {}
            android_path_date_dict["file_path"] = file_path
            android_path_date_dict["last_modified"] = last_modified
            android_path_date_list.append(android_path_date_dict)
        
        pc_path_date_list = []
        if Sync.curr_pc_os == Path.WINDOWS:
            file_list = os.listdir(self.pc_path)
            for file in file_list:
                filename, extension = os.path.splitext(file)
                if not Sync.is_valid_extension(extension):
                    continue
                file_path = os.path.join(self.pc_path, file)
                last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")
                
                pc_path_date_dict = {}
                pc_path_date_dict["file_path"] = file_path
                pc_path_date_dict["last_modified"] = last_modified
                pc_path_date_list.append(pc_path_date_dict)

        elif Sync.curr_pc_os == Path.LINUX:
                file_list = os.listdir(self.pc_path)
                for file in file_list:
                    filename, extension = os.path.splitext(file)
                    if not Sync.is_valid_extension(extension):
                        continue
                    file_path = os.path.join(self.pc_path, file)
                    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")

                    pc_path_date_dict = {}
                    pc_path_date_dict["file_path"] = file_path
                    pc_path_date_dict["last_modified"] = last_modified
                    pc_path_date_list.append(pc_path_date_dict)

        '''Compares the dictionaries in a list, if a pair is found then the the latest last modification 
            date will overwrite to the other platform. If a unique file is found, then it will be copied over.'''
        
        copy_to_android = []
        copy_to_pc = []
        
        for pc_path_date in pc_path_date_list:
            pc_date = pc_path_date["last_modified"]
            pc_path = pc_path_date["file_path"]
            for android_path_date in android_path_date_list:
                android_date = android_path_date["last_modified"]
                android_path = android_path_date["file_path"]

                if os.path.basename(pc_path) == os.path.basename(android_path):
                    if pc_date > android_date:
                        copy_to_android.append(pc_path)
                    elif pc_date < android_date:
                        copy_to_pc.append(android_path)
                    break 

        for android_path_date in android_path_date_list:
            android_path = android_path_date["file_path"]
            android_filename = os.path.basename(android_path)
            if not any(android_filename == os.path.basename(entry["file_path"]) for entry in pc_path_date_list):
                print(f"A new file is synced from android: {android_path}")
                copy_to_pc.append(android_path)

        for pc_path_date in pc_path_date_list:
            pc_path = pc_path_date["file_path"]
            pc_filename = os.path.basename(pc_path)
            if not any(pc_filename == os.path.basename(entry["file_path"]) for entry in android_path_date_list):
                print(f"A new file is synced from pc: {pc_path}")
                copy_to_android.append(pc_path)
        
        '''Does the neccessary file transfers based on the newly created lists'''
        Sync.pull_files_from_android(copy_to_pc)
        Sync.push_files_to_android(copy_to_android)
    
# END==================================================#SYNC OPERATION====================================================#
    