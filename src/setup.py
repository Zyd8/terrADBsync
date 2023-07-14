from datetime import datetime
import os
import subprocess

from src.errorhandler import ErrorHandler 

class Setup():


    # Variables also utilized by Sync and Backup
    current_pc_os = ""
    adb_path = ""
    current_pc_rootpath = ""
    current_android_rootpath = ""
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


    @staticmethod
    @ErrorHandler.handle_error
    def check_android_dir(path):
        """Checks android path that is supposed to exist, if not, terminate"""
        Setup.do_adb(["shell", "ls",  path])

    @staticmethod
    @ErrorHandler.handle_error
    def check_pc_dir(path):
        """Checks pc path that is supposed to exist, if not, terminate"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required directory: {path} on PC does not exist")
        

    @staticmethod
    @ErrorHandler.handle_error 
    def do_adb(command):
        """Does the default repetitive subprocess.run method"""
        adb_command = [Setup.adb_path] + command
        process = subprocess.run(adb_command, capture_output=True, text=True)
        if process.stderr:
            raise subprocess.CalledProcessError(returncode=process.returncode, cmd=adb_command)
        return process


    @staticmethod
    @ErrorHandler.handle_error
    def is_valid_extension(extension):
        """Filter files allowing only Players/Worlds specific extensions"""
        allowed_extensions = (".bak", ".plr", ".wld")
        if extension.lower() in allowed_extensions:
            return True
        return False


