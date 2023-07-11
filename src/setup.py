from datetime import datetime
import os
import subprocess

from errorhandler import ErrorHandler 

class Setup():

    current_pc_os = ""
    current_pc_rootpath = ""
    current_android_rootpath = ""
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    @staticmethod
    def is_valid_extension(extension):
        allowed_extensions = (".bak", ".plr", ".wld")
        if extension.lower() in allowed_extensions:
            return True
        return False

    @staticmethod
    @ErrorHandler.handle_setupclass
    def check_pc_dir(path):
        """Checks pc path that is supposed to exist, if not, terminate"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Terraria subpath: '{os.path.basename(path)}' on PC does not exist")
        
    @staticmethod
    @ErrorHandler.handle_setupclass
    def check_android_dir(path):
        """Checks android path that is supposed to exist, if not, terminate"""
        command = ["adb", "shell", "ls",  path]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.stderr:
            print("Error:", process.stderr)
            raise subprocess.CalledProcessError(f"Terraria subpath: '{os.path.basename(path)}' on android does not exist")