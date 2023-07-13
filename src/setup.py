from datetime import datetime
import os
import subprocess

from errorhandler import ErrorHandler 

class Setup():

    current_pc_os = ""
    adb_path = ""
    current_pc_rootpath = ""
    current_android_rootpath = ""
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def do_adb(command):
        return subprocess.run([Setup.adb_path] + command, capture_output=True, text=True)

    @staticmethod
    def is_valid_extension(extension):
        allowed_extensions = (".bak", ".plr", ".wld")
        if extension.lower() in allowed_extensions:
            return True
        return False

    @staticmethod
    def check_pc_dir(path):
        """Checks pc path that is supposed to exist, if not, terminate"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required directory: {path} on PC does not exist")
        
    @staticmethod
    def check_android_dir(path):
        """Checks android path that is supposed to exist, if not, terminate"""
        process = Setup.do_adb(["shell", "ls",  path])
        if process.stderr:
            print("Error:", process.stderr)
            raise RuntimeError(f"Required directory: {path} on android does not exist")