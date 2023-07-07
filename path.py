import os
import sys
import subprocess

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
            for path in default_paths:
                if os.path.exists(path):
                    Setup.current_pc_rootpath = path
                    print("Default directory found")
                    found_path = True
                    break
                elif os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        Setup.current_pc_rootpath = f.readline().strip()
                    print("Custom directory found")
                    found_path = True
                    break

        elif Setup.current_pc_os == Path.LINUX:
            default_paths = [os.path.expanduser("~/.local/share/Terraria"),
                             os.path.expanduser("~/.var/app/com.valvesoftware.Steam/.local/share/Terraria")]
            for path in default_paths:
                if os.path.exists(path):
                    Setup.current_pc_rootpath = path
                    print("Default directory found")
                    found_path = True
                    break
                elif os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        Setup.current_pc_rootpath = f.readline().strip()
                    print("Custom directory found")
                    found_path = True
                    break

        if not found_path:
            Path.pc_custom_path()

    @staticmethod
    def set_android_terraria_rootpath():
        default_path = "sdcard/Android/data/com.and.games505.TerrariaPaid"
        command = ["adb", "shell", "ls",  default_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Terrariad default path on android does not exist")
            print("Error:", error.decode())
        else:
            Setup.current_android_rootpath = default_path
        
    @staticmethod
    def pc_custom_path():
        config_path = os.path.join(os.getcwd(), "custom_path.txt")

        path = input("Default directory not found in PC.\nYou can enter the custom path of where you have set the Terraria directory.\nExample: path/to/'Terraria'.\nPress 'q' to terminate program.\n")

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
            print("Custom directory remembered")
