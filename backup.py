import subprocess
import shutil
from datetime import datetime
from enums import *

class Backup:

    curr_pc_os = ""
    curr_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def __init__(self, pc, android):
        self.pc = pc
        self.android = android 
        
    def backup_pc_files(self):
        file_list = os.listdir(self.pc)
        for file in file_list:
            if Backup.curr_pc_os == Path.WINDOWS.value:
                source_path = os.path.join(self.pc, file)
                destination_path = os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), os.path.basename(self.pc), file)
                base_name, extension = os.path.splitext(destination_path)
    
            elif Backup.curr_pc_os == Path.LINUX.value:
                source_path = os.path.join(self.pc, file)
                destination_path = os.path.join(Path.LINUX.get_terraria_backup_root_dir(), os.path.basename(self.pc), file)
                base_name, extension = os.path.splitext(destination_path)
                
            shutil.copy(source_path, f"{base_name}[{Backup.curr_datetime}]{extension}")
            
    def backup_android_files(self):
        command = ["adb", "shell", "ls", self.android]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            source_path = os.path.join(self.android, file).replace("\\", "/")
            destination_path = os.path.join(Path.ANDROID.get_terraria_backup_root_dir(), os.path.basename(self.android), file).replace("\\", "/")
            base_name, extension = os.path.splitext(destination_path)
            command = ["adb", "shell", "cp", source_path, f"{base_name}[{Backup.curr_datetime}]{extension}"]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout)
            if process.stderr:
                print("Error:", process.stderr)

    @staticmethod
    def check_pc_backup_dir():
        if Backup.curr_pc_os == Path.WINDOWS.value:
            for path in Path.WINDOWS.get_terraria_backup_array_dir():
                if not os.path.exists(path):
                    Backup.make_pc_backup_dir(path)
                    print(f"PC backup: {path} folder is created")

        if Backup.curr_pc_os == Path.LINUX.value:
            for path in Path.LINUX.get_terraria_backup_array_dir():
                if not os.path.exists(path):
                    Backup.make_pc_backup_dir(path)
                    print(f"PC backup: {path} folder is created")
            
    @staticmethod
    def check_android_backup_dir():
        for path in Path.ANDROID.get_terraria_backup_array_dir():
            command = ["adb", "shell", "ls", path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0 and not process.stdout:
                print(f"Android backup: {path} folder is created")
                Backup.make_android_backup_dir(path)

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