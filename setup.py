from datetime import datetime
import os
import time
import sys
import subprocess

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
    def check_pc_dir(path):
        """Checks pc path that is supposed to exist, if not, terminate"""
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Error: Terraria subpath: '{os.path.basename(path)}' on PC does not exist")
        except FileNotFoundError as e:
            print(str(e))
            time.sleep(3)
            sys.exit(0)
        
    @staticmethod
    def check_android_dir(path):
        """Checks android path that is supposed to exist, if not, terminate"""
        command = ["adb", "shell", "ls",  path]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if error:
                raise subprocess.CalledProcessError(error)
        except subprocess.CalledProcessError as e:
            print(f"Error: Terraria subpath: '{os.path.basename(path)}' on android does not exist")
            print("Error:", e.output.decode())
            time.sleep(3)
            sys.exit(0)