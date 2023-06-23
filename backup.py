import subprocess
import shutil
from datetime import datetime
from enums import *

class Backup:

    curr_pc_os = ""
    curr_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def __init__(self, android_dir, pc_dir):
        self.android_dir = android_dir 
        self.pc_dir = pc_dir

    @staticmethod
    def is_file_valid(extension):
        allowed_extensions = (".bak", ".plr", ".wld")
        if extension.lower() in allowed_extensions:
            return True
        return False
    
    def execute_backup(self):

        android_backup_root_dir = os.path.join(Path.ANDROID.get_terraria_backup_root_dir(), Backup.curr_datetime).replace("\\", "/")
        Backup.check_android_backup_dir(android_backup_root_dir)

        android_backup_branch_dir = os.path.join(android_backup_root_dir, os.path.basename(self.android_dir)).replace("\\", "/")
        Backup.check_android_backup_dir(android_backup_branch_dir)

        command = ["adb", "shell", "ls", self.android_dir]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if Backup.is_file_valid(extension):
                source_path = os.path.join(self.android_dir, file).replace("\\", "/")
                destination_path = os.path.join(android_backup_branch_dir, file).replace("\\", "/")
                command = ["adb", "shell", "cp", source_path, destination_path]
                process = subprocess.run(command, capture_output=True, text=True)
                if process.stdout:
                    print("Output:", process.stdout)
                if process.stderr:
                    print("Error:", process.stderr)
        
        pc_backup_root_dir = os.path.join(Backup.curr_pc_os.get_terraria_backup_root_dir(), Backup.curr_datetime)
        Backup.check_pc_backup_dir(pc_backup_root_dir)

        pc_backup_branch_dir = os.path.join(pc_backup_root_dir, os.path.basename(self.pc_dir))
        Backup.check_pc_backup_dir(pc_backup_branch_dir)

        file_list = os.listdir(self.pc_dir)
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if Backup.is_file_valid(extension):
                if Backup.curr_pc_os == Path.WINDOWS:
                    source_path = os.path.join(self.pc_dir, file)
                    destination_path = os.path.join(pc_backup_branch_dir, file)
        
                elif Backup.curr_pc_os == Path.LINUX:
                    source_path = os.path.join(self.pc_dir, file)
                    destination_path = os.path.join(pc_backup_branch_dir, file)

                shutil.copy(source_path, destination_path)

    @staticmethod
    def check_pc_backup_dir(directory):
        if not os.path.exists(directory):
            Backup.make_pc_backup_dir(directory)
            print(f"PC backup: {directory} folder is created")
            
    @staticmethod
    def check_android_backup_dir(directory):
            command = ["adb", "shell", "ls", directory]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0 and not process.stdout:
                print(f"Android backup: {directory} folder is created")
                Backup.make_android_backup_dir(directory)

    @staticmethod
    def make_pc_backup_dir(directory):
        try:
            os.makedirs(directory)
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