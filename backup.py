import subprocess
import shutil
import os

from path import Path
from setup import Setup

class Backup(Setup):

    def __init__(self, android_path, pc_path):
        self.android_path = android_path 
        self.pc_path = pc_path

    def handle_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                print(f"Error: File not found error: {e}")
                Backup.with_error_terminate()
            except subprocess.CalledProcessError as e:
                print(f"Error: Failed to execute adb command {e}")
                Backup.with_error_terminate()
            except subprocess.TimeoutExpired:
                print(f"Error: adb command timed out")
                Backup.with_error_terminate()
            except OSError as e:
                print(f"Error: Failed to create folder: {e}")
                Backup.with_error_terminate()
            except Exception as e:
                print(f"Error: An unexpected error occurred: {e}")
                Backup.with_error_terminate()
        return wrapper

    @staticmethod
    @handle_exceptions
    def set_pc_dir(path):
        """Set empty pc folder for filling"""
        if not os.path.exists(path):
            os.makedirs(path)        
            print(f"PC backup: {path} folder is created")
    
    @staticmethod
    @handle_exceptions
    def set_android_dir(path):
        """Set empty android folder for filling"""
        command = ["adb", "shell", "ls", path]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0 and not process.stdout:
            command = ["adb", "shell", "mkdir", path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout)
            if process.stderr:
                print("Error:", process.stderr)     
            else:
                print(f"Android backup: {path} folder is created")
                
    @handle_exceptions
    def set_unique_dir(self):
        """Set an empty unique backup folder tree in the 'backups' folder"""
        android_rootpath = os.path.join(Path.ANDROID.get_terraria_backup_rootpath(), Backup.current_datetime).replace("\\", "/")
        Backup.set_android_dir(android_rootpath)
        android_subpath = os.path.join(android_rootpath, os.path.basename(self.android_path)).replace("\\", "/")
        Backup.set_android_dir(android_subpath)
        pc_rootpath = os.path.join(Backup.current_pc_os.get_terraria_backup_rootpath(), Backup.current_datetime)
        Backup.set_pc_dir(pc_rootpath)
        pc_subpath = os.path.join(pc_rootpath, os.path.basename(self.pc_path))
        Backup.set_pc_dir(pc_subpath)

        return android_subpath, pc_subpath
    
    @handle_exceptions
    def fill_unique_dir(self, android_subpath, pc_subpath):
        """Fills up the empty unique backup folder tree in the 'backups' folder"""
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
                source_path = os.path.join(self.pc_path, file)
                destination_path = os.path.join(pc_subpath, file)
                shutil.copy(source_path, destination_path)
    
    def execute_backup(self):
        android_subpath, pc_subpath = Backup.set_unique_dir(self)
        Backup.fill_unique_dir(self, android_subpath, pc_subpath)

        