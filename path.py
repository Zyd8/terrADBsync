import os
import sys
import subprocess
import time

from enum import Enum
from setup import Setup

class Path(Enum):

    WINDOWS = "Windows"
    LINUX = "Linux"
    ANDROID = "Android"

    def get_terraria_rootpath(self):
        if self == Path.WINDOWS or self == Path.LINUX:
            return Setup.current_pc_rootpath
        elif self == Path.ANDROID:
            return Setup.current_android_rootpath
        
    def get_terraria_array_subpath(self):
        if self == Path.WINDOWS:
            return [os.path.join(Path.WINDOWS.get_terraria_rootpath(), "Players"), 
                    os.path.join(Path.WINDOWS.get_terraria_rootpath(), "Worlds")]
        elif self == Path.LINUX:
            return [f"{Path.LINUX.get_terraria_rootpath()}/Players", 
                    f"{Path.LINUX.get_terraria_rootpath()}/Worlds"]
        elif self == Path.ANDROID:
            return [f"{Path.ANDROID.get_terraria_rootpath()}/Players", 
                    f"{Path.ANDROID.get_terraria_rootpath()}/Worlds"]
    
    def get_terraria_backup_rootpath(self):
        if self == Path.WINDOWS:
            return os.path.join(Path.WINDOWS.get_terraria_rootpath(), "backups")
        elif self == Path.LINUX:
            return f"{Path.LINUX.get_terraria_rootpath()}/backups"
        elif self == Path.ANDROID:
            return f"{Path.ANDROID.get_terraria_rootpath()}/backups"
    
    @staticmethod
    def set_pc_terraria_rootpath():
        """Check pc default paths then custom paths configuration file, else, prompt for a custom path"""
        config_path = os.path.join(os.getcwd(), "custom_path.txt")
        found_path = False
        
        if Setup.current_pc_os == Path.WINDOWS:
            default_paths = [os.path.join(os.environ["UserProfile"], "Documents", "My Games", "Terraria")]
        elif Setup.current_pc_os == Path.LINUX:
            default_paths = [os.path.expanduser("~/.local/share/Terraria"),
                             os.path.expanduser("~/.var/app/com.valvesoftware.Steam/.local/share/Terraria")]
            
        for path in default_paths:
            if os.path.exists(path):
                Setup.current_pc_rootpath = path
                print("Default directory found")
                found_path = True
                break

        if not found_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                custom_path = f.readline().strip()
                if os.path.exists(custom_path):
                    print(custom_path)
                    Setup.current_pc_rootpath = custom_path
                    print("Custom directory found")
                    found_path = True
        elif not found_path:
            Path.pc_custom_path()

    @staticmethod
    def set_android_terraria_rootpath():
        default_path = "sdcard/Android/data/com.and.games505.TerrariaPaid"
        command = ["adb", "shell", "ls",  default_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Error:", error.decode())
            raise RuntimeError("Terraria default path on Android does not exist")
        else:
            Setup.current_android_rootpath = default_path

    @staticmethod
    def pc_custom_path():
        config_path = os.path.join(os.getcwd(), "custom_path.txt")
        try:
            path = input("Terraria directory not found in PC.\nYou can enter the custom path of where you have set the Terraria directory.\nExample: path/to/'Terraria'.\nPress 'q' to terminate program.\n")
            if path.lower() == "q":
                sys.exit(0)
            elif os.path.basename(path) != "Terraria":
                raise SyntaxError("The inputted path must end with 'Terraria'")
            else: 
                if os.path.exists(path):
                    print("Custom directory found")
                    with open(config_path, "w") as f:
                        f.write(path)
                    Setup.current_pc_rootpath = path
                else: 
                    raise FileNotFoundError("The input path does not exist.")
                print("Custom directory remembered")
        except (FileNotFoundError, SyntaxError) as e:
            Path.pc_custom_path()
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            time.sleep(3)
            sys.exit(0)
