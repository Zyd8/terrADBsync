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

    def handle_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                print(f"File not found error: {e}")
                Setup.with_error_terminate()
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute adb command {e}")
                Setup.with_error_terminate()
            except subprocess.TimeoutExpired:
                print(f"adb command timed out")
                Setup.with_error_terminate()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                Setup.with_error_terminate()
        return wrapper

    @staticmethod
    def is_valid_extension(extension):
        allowed_extensions = (".bak", ".plr", ".wld")
        if extension.lower() in allowed_extensions:
            return True
        return False

    @staticmethod
    @handle_exceptions
    def check_pc_dir(path):
        """Checks pc path that is supposed to exist, if not, terminate"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Terraria subpath: '{os.path.basename(path)}' on PC does not exist")
        
    @staticmethod
    @handle_exceptions
    def check_android_dir(path):
        """Checks android path that is supposed to exist, if not, terminate"""
        command = ["adb", "shell", "ls",  path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Error:", error.decode())
            raise subprocess.CalledProcessError(f"Terraria subpath: '{os.path.basename(path)}' on android does not exist")

    @staticmethod
    def with_error_terminate():
        time.sleep(3)
        sys.exit(1)
    
    @staticmethod
    def no_error_terminate():
        sys.exit(0)