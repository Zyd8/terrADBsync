import subprocess
import shutil
from datetime import datetime
from enums import *

class Backup:

# START==================================================GlOBAL VARIABLES===================================================#

    curr_pc_os = ""
    curr_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# END==================================================GlOBAL VARIABLES=====================================================#

# START================================================BACKUP UTILS=========================================================#

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
    def check_pc_dir(path):
        if not os.path.exists(path):
            Backup.make_pc_dir(path)
            print(f"PC backup: {path} folder is created")
            
    @staticmethod
    def check_android_dir(path):
        command = ["adb", "shell", "ls", path]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0 and not process.stdout:
            print(f"Android backup: {path} folder is created")
            Backup.make_android_dir(path)

    @staticmethod
    def make_pc_dir(path):
        try:
            os.makedirs(path)
        except OSError as e:
            print(f"Failed to create folder: {e}")

    @staticmethod
    def make_android_dir(path):
        command = ["adb", "shell", "mkdir", path]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.stdout:
            print("Output:", process.stdout)
        if process.stderr:
            print("Error:", process.stderr)

# END==================================================BACKUP UTILS=========================================================#

# START================================================BACKUP OPERATION======================================================#
    
    def execute_backup(self):

        android_rootpath = os.path.join(Path.ANDROID.get_terraria_backup_rootpath(), Backup.curr_datetime).replace("\\", "/")
        Backup.check_android_dir(android_rootpath)
        pc_rootpath = os.path.join(Backup.curr_pc_os.get_terraria_backup_rootpath(), Backup.curr_datetime)
        Backup.check_pc_dir(pc_rootpath)

        android_subpath = os.path.join(android_rootpath, os.path.basename(self.android_path)).replace("\\", "/")
        Backup.check_android_dir(android_subpath)
        pc_subpath = os.path.join(pc_rootpath, os.path.basename(self.pc_path))
        Backup.check_pc_dir(pc_subpath)

        command = ["adb", "shell", "ls", self.android_path]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if Backup.is_valid_extension(extension):
                source_path = os.path.join(self.android_path, file).replace("\\", "/")
                destination_path = os.path.join(android_subpath, file).replace("\\", "/")
                command = ["adb", "shell", "cp", source_path, destination_path]
                process = subprocess.run(command, capture_output=True, text=True)
                if process.stdout:
                    print("Output:", process.stdout)
                if process.stderr:
                    print("Error:", process.stderr)

        file_list = os.listdir(self.pc_path)
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if Backup.is_valid_extension(extension):
                if Backup.curr_pc_os == Path.WINDOWS:
                    source_path = os.path.join(self.pc_path, file)
                    destination_path = os.path.join(pc_subpath, file)
        
                elif Backup.curr_pc_os == Path.LINUX:
                    source_path = os.path.join(self.pc_path, file)
                    destination_path = os.path.join(pc_subpath, file)

                shutil.copy(source_path, destination_path)

# END================================================BACKUP OPERATION======================================================#