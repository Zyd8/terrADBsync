import os
import subprocess
from enums import Path
from enums import Commands

class Sync:
    
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

    # From PC to Android
    def adb_push_directory(self):

        Sync.check_pc_dir(self.pc)
        Sync.check_adb_dir(self.android)
        self.check_android_backup_dir()
        self.check_pc_backup_dir()

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
        
    # From Android to PC
    def adb_pull_directory(self):

        Sync.check_pc_dir(self.pc)
        Sync.check_adb_dir(self.android) 
        self.check_android_backup_dir()
        self.check_pc_backup_dir()

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
    
    def check_pc_backup_dir(self):
        if Sync.curr_pc_os == Path.WINDOWS.value:
            if not os.path.exists(Path.WINDOWS.get_terraria_backup_root_dir()):

                Sync.make_pc_backup_dir(Path.WINDOWS.get_terraria_backup_root_dir())
                print("PC backup root folder is created as it does not exist")

            elif self.pc == Path.WINDOWS.get_terraria_player_dir() or self.pc == Path.WINDOWS.get_terraria_world_dir():
                if not os.path.exists(os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), self.get_pc_end_path())):

                    Sync.make_pc_backup_dir(os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), self.get_pc_end_path()))
                    print("PC backup branch folder is created as it does not exist")
            
        if Sync.curr_pc_os == Path.LINUX.value:
            if not os.path.exists(Path.LINUX.get_terraria_backup_root_dir()):

                Sync.make_pc_backup_dir(Path.LINUX.get_terraria_backup_root_dir())
                print("PC backup root folder is created as it does not exist")

            elif self.pc == Path.LINUX.get_terraria_player_dir() or self.pc == Path.LINUX.get_terraria_world_dir():
                if not os.path.exists(os.path.join(Path.LINUX.get_terraria_backup_root_dir(), self.get_pc_end_path())):

                    Sync.make_pc_backup_dir(Path.LINUX.get_terraria_backup_root_dir(), self.get_pc_end_path())
                    print("PC backup branch folder is created as it does not exist")
            
    def check_android_backup_dir(self):
        backup_root_path = os.path.join(Path.ANDROID.get_terraria_root_dir(), "backups").replace("\\", "/")
        command = ["adb", "shell", "ls", backup_root_path]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0 and not process.stdout:
            print("Android backup root folder is created as it does not exist")
            Sync.make_android_backup_dir(backup_root_path)
        else:
            backup_branch_path = os.path.join(Path.ANDROID.get_terraria_root_dir(), "backups", self.get_android_end_path()).replace("\\", "/")
            command = ["adb", "shell", "ls", backup_branch_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0 and not process.stdout:
                print("Android backup branch folder is created as it does not exist")
                Sync.make_android_backup_dir(backup_branch_path)

    @staticmethod
    def make_pc_backup_dir(directory):
        try:
            os.makedirs(directory)
            print("Folder created successfully.")
        except OSError as e:
            print(f"Failed to create folder: {e}")

    @staticmethod
    def make_android_backup_dir(directory):
        command = ["adb", "shell", "mkdir", directory]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.stdout:
            print("Output:", process.stdout)
        if process.stderr:
            print("Error:", process.stderr)
            
        


