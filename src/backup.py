import subprocess
import shutil
import os

from path import Path
from setup import Setup
from errorhandler import ErrorHandler

class Backup(Setup):

    def __init__(self, android_path, pc_path):
        self.android_path = android_path 
        self.pc_path = pc_path

    @staticmethod
    @ErrorHandler.handle_backupclass
    def set_pc_dir(path):
        """Set empty pc folder for filling"""
        if not os.path.exists(path):
            os.makedirs(path)    
            print(f"PC backup: {os.path.basename(path)} folder is created")    
    
    @staticmethod
    @ErrorHandler.handle_backupclass
    def set_android_dir(path):
        """Set empty android folder for filling"""
        command = ["adb", "shell", "ls", path]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0 and not process.stdout:
            command = ["adb", "shell", "mkdir", path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stderr:
                print("adb error in setting unique backup folder:", process.stderr)     
            else:
                print(f"Android backup: {os.path.basename(path)} folder is created")
                
    @ErrorHandler.handle_backupclass
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
    
    @ErrorHandler.handle_backupclass
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
                if process.stderr:
                    print("adb error in filling unique backup folder:", process.stderr)

        file_list = os.listdir(self.pc_path)
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if Backup.is_valid_extension(extension):
                source_path = os.path.join(self.pc_path, file)
                destination_path = os.path.join(pc_subpath, file)
                shutil.copy(source_path, destination_path)

    def remove_old_archives():

        # PC side
        folder_list = os.listdir(Backup.current_pc_os.get_terraria_backup_rootpath())
        if len(folder_list) > 5:
            last_folder_namepath = os.path.join(Backup.current_pc_os.get_terraria_backup_rootpath(), folder_list[0])
            shutil.rmtree(last_folder_namepath)

        # Android side
        command = ["adb", "shell", "ls", Path.ANDROID.get_terraria_backup_rootpath()]
        process = subprocess.run(command, capture_output=True, text=True)
        folder_list = process.stdout.splitlines()
        if len(folder_list) > 5:
            last_folder_namepath = os.path.join(Path.ANDROID.get_terraria_backup_rootpath(), folder_list[0]).replace("\\", "/")
            command = ["adb", "shell", "rm", "-r", last_folder_namepath]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stderr:
                print("adb error in removing old archives: ", process.stderr)

    def execute_backup(self):
        android_subpath, pc_subpath = Backup.set_unique_dir(self)
        Backup.fill_unique_dir(self, android_subpath, pc_subpath)
        