import sys
import os
import subprocess
from terradbsync_enums import Path
from terradbsync_enums import Commands

class Sync_Manager:
    
    curr_pc_os = ""

    def __init__(self, pc, android):
        self.pc = pc
        self.android = android 

    def get_pc_end_path(self):
        slash_list = []
        for index, slash in enumerate(self.pc):
            if slash == "\\":
                slash_list.append(index)
        return self.pc[max(slash_list)+1::]
        
    def get_android_end_path(self):
        slash_list = []
        for index, slash in enumerate(self.android):
            if slash == "/":
                slash_list.append(index)
        return self.android[max(slash_list)+1::]

    @staticmethod
    def check_pc_os():
        if os.name == "nt":
            Sync_Manager.curr_pc_os = Path.WINDOWS.value
            return Path.WINDOWS
        elif os.name == "posix":
            Sync_Manager.curr_pc_os = Path.LINUX.value
            return Path.LINUX
        else:
            print("The PC operating system is not supported")
            sys.exit(0)

    @staticmethod
    def check_adb():
        output = subprocess.check_output(["adb", "devices"]).decode()
        lines = output.strip().split('\n')
        if len(lines) > 1:
            devices = lines[1:]
            for device in devices:
                if "device" in device:
                    return True
        print("android device cannot be found through adb connection")
        return False

    @staticmethod
    def check_pc_dir(directory):
        if os.path.exists(directory):
            return True
        else:
            print("Terraria directory on PC does not exist")
            return False
    
    @staticmethod 
    def check_adb_dir(self):
        command = ["adb", "shell", "ls",  self]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Terraria directory on android does not exist")
            print("Error:", error.decode())
            return False
        return True

    # From PC to Android
    def adb_push_directory(self):
        print(self.pc)
        Sync_Manager.check_pc_dir(self.pc)
        Sync_Manager.check_adb_dir(self.android)
        self.check_pc_backup()
        #Sync_Manager.check_android_backup_dir()
        file_list = os.listdir(self.pc)
        for file in file_list:
            source_path = os.path.join(self.pc, file)
            destination_path = self.android
            command = ["adb", "push", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout)
            if process.stderr:
                print("Error:", process.stderr)
                return False
        return True
        
    # From Android to PC
    def adb_pull_directory(self):
        Sync_Manager.check_pc_dir(self.pc)
        Sync_Manager.check_adb_dir(self.android)
        self.check_pc_backup()
        #Sync_Manager.check_android_backup_dir()
        command = ["adb", "shell", "ls", self.android]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            source_path = os.path.join(self.android, file).replace("\\", "/")
            destination_path = self.pc
            command = ["adb", "pull", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout)
            if process.stderr:
                print("Error:", process.stderr)
                return False
        return True
    

    def check_pc_backup(self):
        if Sync_Manager.curr_pc_os == Path.WINDOWS.value:
            if not os.path.exists(Path.WINDOWS.get_terraria_backup_root_dir()):
                Sync_Manager.make_pc_backup_dir(Path.WINDOWS.get_terraria_backup_root_dir())
            elif self.pc == Path.WINDOWS.get_terraria_player_dir() or self.pc == Path.WINDOWS.get_terraria_world_dir():
                if not os.path.exists(os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), self.get_pc_end_path())):
                    Sync_Manager.make_pc_backup_dir(os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), self.get_pc_end_path()))
            
        if Sync_Manager.curr_pc_os == Path.LINUX.value:
            if not os.path.exists(Path.LINUX.get_terraria_backup_root_dir()):
                Sync_Manager.make_pc_backup_dir(Path.LINUX.get_terraria_backup_root_dir())
            elif self.pc == Path.LINUX.get_terraria_player_dir() or self.pc == Path.LINUX.get_terraria_world_dir():
                if not os.path.exists(os.path.join(Path.LINUX.get_terraria_backup_root_dir(), self.get_pc_end_path())):
                    Sync_Manager.make_pc_backup_dir(Path.LINUX.get_terraria_backup_root_dir(), self.get_pc_end_path())
            
    @staticmethod
    def check_android_backup_dir():
        command = ["adb", "shell", "ls", os.path.join(Path.ANDROID.get_terraria_root_dir(), "backups").replace("\\", "/")]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0 or not process.stdout:
            Sync_Manager.make_android_backup_dir()
    
    @staticmethod
    def make_pc_backup_dir(directory):
        try:
                os.makedirs(directory)
                print("Folder created successfully.")
                
        except OSError as e:
            print(f"Failed to create folder: {e}")

    @staticmethod
    def make_android_backup_dir():
        command = ["adb", "shell", "mkdir", os.path.join(Path.ANDROID.get_terraria_root_dir(), "backups").replace("\\", "/")]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.stdout:
            print("Output:", process.stdout)
        if process.stderr:
            print("Error:", process.stderr)
            
        


