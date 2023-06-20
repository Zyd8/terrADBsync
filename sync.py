import os
import subprocess
from enums import Path

class Sync:
    
    curr_pc_os = ""

    def __init__(self, pc, android):
        self.pc = pc
        self.android = android 

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

    # From PC to Android
    def adb_push_directory(self):

        Sync.check_pc_dir(self.pc)
        Sync.check_adb_dir(self.android)

        file_list = os.listdir(self.pc)
        for file in file_list:
            source_path = os.path.join(self.pc, file)
            destination_path = self.android
            command = ["adb", "push", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout, end="")
            if process.stderr:
                print("Error:", process.stderr, end="")
        
    # From Android to PC
    def adb_pull_directory(self):

        Sync.check_pc_dir(self.pc)
        Sync.check_adb_dir(self.android) 

        command = ["adb", "shell", "ls", self.android]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            source_path = os.path.join(self.android, file).replace("\\", "/")
            destination_path = self.pc
            command = ["adb", "pull", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout, end="")
            if process.stderr:
                print("Error:", process.stderr, end="")
            
        


