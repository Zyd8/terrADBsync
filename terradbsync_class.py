import sys
import os
import subprocess
from terradbsync_enums import Operating_System
   
class Sync_Manager:

    def __init__(self, pc, mobile):
        self.__pc = pc
        self.__mobile = mobile

    @property
    def pc(self):
        return self.__pc

    @property
    def mobile(self):
        return self.__mobile
    
    @staticmethod
    def check_pc_os():
        if os.name == "nt":
            return Operating_System.WINDOWS
        elif os.name == "posix":
            return Operating_System.LINUX
        else:
            print("The PC operating system is not supported")
            sys.exit(0)

    @staticmethod
    def check_pc_dir(directory):
        if os.path.exists(directory):
            return True
        else:
            print("Terraria directory on PC does not exist or moved by the user")
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
        print("Mobile device cannot be found through adb connection")
        return False

    @staticmethod
    def check_adb_dir(directory):
        command = ["adb", "shell", "ls", directory]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Terraria directory on mobile does not exist or moved by the user")
            print("Error:", error.decode())
            return False
        return True

    # Files from PC to mobile
    def adb_push_directory(self):
        Sync_Manager.check_pc_dir(self.pc)
        Sync_Manager.check_adb_dir(self.mobile)
        file_list = os.listdir(self.pc)
        for file_name in file_list:
            source_path = os.path.join(self.pc, file_name)
            destination_path = self.mobile
            command = ["adb", "push", source_path, destination_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if output:
                print("Output:", output.decode())
            if error:
                print("Error:", error.decode())
                return False
        return True
        
    # Files from mobile to PC
    def adb_pull_directory(self):
        Sync_Manager.check_pc_dir(self.pc)
        Sync_Manager.check_adb_dir(self.mobile)
        command = ["adb", "shell", "ls", self.mobile]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        file_list = output.decode().splitlines()
        for file_name in file_list:
            source_path = os.path.join(self.mobile, file_name).replace('\\', '/')
            destination_path = self.pc
            command = ["adb", "pull", source_path, destination_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if output:
                print("Output:", output.decode())
            if error:
                print("Error:", error.decode())
                return False
        return True

