import os
import subprocess
from enums import Path
import datetime

class Sync:
    
    curr_pc_os = ""

    def __init__(self, pc, android):
        self.pc = pc
        self.android = android 
    
    @staticmethod
    def is_file_valid(extension):
        allowed_extensions = (".bak", ".plr", ".wld")
        if extension.lower() in allowed_extensions:
            return True
        return False

    @staticmethod
    def check_pc_os():
        if os.name == "posix":
            Sync.curr_pc_os = Path.LINUX.value
            return Path.LINUX
        elif os.name == "nt":
            Sync.curr_pc_os = Path.WINDOWS.value
            return Path.WINDOWS
        else:
            print("The PC operating system is not supported")
            return False

    @staticmethod
    def check_adb():
        output = subprocess.check_output(["adb", "devices"]).decode()
        lines = output.strip().split('\n')
        if len(lines) > 1:
            devices = lines[1:]
            for device in devices:
                if "device" in device:
                    return True        
        print("Android device cannot be found through adb connection")
        return False

    def check_pc_dir(directory):
        if os.path.exists(directory):
            return True
        else:
            print("Terraria directory on PC does not exist")
            return False
    
    def check_adb_dir(directory):
        command = ["adb", "shell", "ls",  directory]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Terraria directory on android does not exist")
            print("Error:", error.decode())
            return False
        return True
    
    # START=======================================================MANUAL SYNC OPERATIONS====================================================#

    # From PC to Android
    def adb_push_files(self):

        Sync.check_pc_dir(self.pc)
        Sync.check_adb_dir(self.android)

        file_list = os.listdir(self.pc)
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if Sync.is_file_valid(extension):
                source_path = os.path.join(self.pc, file)
                destination_path = self.android
                command = ["adb", "push", source_path, destination_path]
                process = subprocess.run(command, capture_output=True, text=True)
                if process.stdout:
                    print("Output:", process.stdout, end="")
                if process.stderr:
                    print("Error:", process.stderr, end="")
        
    # From Android to PC
    def adb_pull_files(self):

        Sync.check_pc_dir(self.pc)
        Sync.check_adb_dir(self.android) 

        command = ["adb", "shell", "ls", self.android]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if Sync.is_file_valid(extension):
                source_path = os.path.join(self.android, file).replace("\\", "/")
                destination_path = self.pc
                command = ["adb", "pull", source_path, destination_path]
                process = subprocess.run(command, capture_output=True, text=True)
                if process.stdout:
                    print("Output:", process.stdout, end="")
                if process.stderr:
                    print("Error:", process.stderr, end="")

    # END=======================================================MANUAL SYNC OPERATIONS====================================================#

    # START==================================================AUTOMATIC SYNC OPERATIONS====================================================#
    def adb_auto_sync():
        '''Extracts the file paths and its respective last modified dates, placing it in a dictionary, then to a list.'''

        android_path_date_list = []
        for root_path in Path.ANDROID.get_terraria_array_dir():
            Sync.check_adb_dir(root_path)
            command = ["adb", "shell", "ls", root_path]
            process = subprocess.run(command, capture_output=True, text=True)
            file_list = process.stdout.splitlines()
            for file in file_list:
                filename, extension = os.path.splitext(file)
                if not Sync.is_file_valid(extension):
                    continue
                file_path =  os.path.join(root_path, file).replace("\\", "/")
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
        if Sync.curr_pc_os == Path.WINDOWS.value:
            for root_path in Path.WINDOWS.get_terraria_array_dir():
                Sync.check_pc_dir(root_path)
                file_list = os.listdir(root_path)
                for file in file_list:
                    filename, extension = os.path.splitext(file)
                    if not Sync.is_file_valid(extension):
                        continue
                    file_path = os.path.join(root_path, file)
                    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")
                    
                    pc_path_date_dict = {}
                    pc_path_date_dict["file_path"] = file_path
                    pc_path_date_dict["last_modified"] = last_modified
                    pc_path_date_list.append(pc_path_date_dict)

        elif Sync.curr_pc_os == Path.LINUX.value:
            for root_path in Path.LINUX.get_terraria_array_dir():
                Sync.check_pc_dir(root_path)
                file_list = os.listdir(root_path)
                for file in file_list:
                    filename, extension = os.path.splitext(file)
                    if not Sync.is_file_valid(extension):
                        continue
                    file_path = os.path.join(root_path, file)
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
                        print("0")
                        copy_to_android.append(pc_path)
                    elif pc_date < android_date:
                        print("1")
                        copy_to_pc.append(android_path)
                    break 

            else:
                print("No match found for PC file:", pc_path)

        for android_path_date in android_path_date_list:
            android_path = android_path_date["file_path"]
            android_filename = os.path.basename(android_path)
            if not any(android_filename == os.path.basename(entry["file_path"]) for entry in pc_path_date_list):
                copy_to_pc.append(android_path)

        for pc_path_date in pc_path_date_list:
            pc_path = pc_path_date["file_path"]
            pc_filename = os.path.basename(pc_path)
            if not any(pc_filename == os.path.basename(entry["file_path"]) for entry in android_path_date_list):
                copy_to_android.append(pc_path)
        
        '''Does the neccessary file transfers based on the newly created lists'''
        Sync.adb_pull_files(copy_to_pc)
        Sync.adb_push_files(copy_to_android)
    
    def get_second_to_last_word(path):
        slash_list = []
        for index, slash in enumerate(path):
            if slash == "\\" or slash == "/":
                slash_list.append(index)
        second_last_slash_index = slash_list[-2] if len(slash_list) >= 2 else -1
        return path[second_last_slash_index+1:max(slash_list)]
    
     # From Android to PC
    @staticmethod
    def adb_pull_files(path_list):
        for path in path_list:
            source_path = path
            if Sync.curr_pc_os == Path.WINDOWS.value:
                destination_path = os.path.join(Path.WINDOWS.get_terraria_root_dir(), Sync.get_second_to_last_word(source_path)).replace("\\", "/")
            elif Sync.curr_pc_os == Path.LINUX.value:
                destination_path = os.path.join(Path.WINDOWS.get_terraria_root_dir(), Sync.get_second_to_last_word(source_path)).replace("\\", "/")
            command = ["adb", "pull", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout, end="")
            if process.stderr:
                print("Error:", process.stderr, end="")

    # From PC to Android
    @staticmethod
    def adb_push_files(path_list):
        for path in path_list:
            source_path = path
            destination_path = os.path.join(Path.ANDROID.get_terraria_root_dir(), Sync.get_second_to_last_word(source_path)).replace("\\", "/")
            command = ["adb", "push", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout, end="")
            if process.stderr:
                print("Error:", process.stderr, end="")

    # END==================================================##AUTOMATIC SYNC OPERATIONS====================================================#
        
            



"""
for pc_path_date in pc_path_date_list:
    pc_date = pc_path_date["last_modified"]
    pc_path = pc_path_date["file_path"]
    
    found_match = False

    for android_path_date in android_path_date_list:
        android_date = android_path_date["last_modified"]
        android_path = android_path_date["file_path"]

        if os.path.basename(pc_path) == os.path.basename(android_path):
            found_match = True
            if pc_date > android_date:
                copy_to_android.append(pc_path)
            elif pc_date < android_date:
                copy_to_pc.append(android_path)

    if not found_match:
        copy_to_android.append(pc_path)

for android_path_date in android_path_date_list:
    android_path = android_path_date["file_path"]
    if not any(android_path == entry["file_path"] for entry in pc_path_date_list):
        copy_to_pc.append(android_path)

"""