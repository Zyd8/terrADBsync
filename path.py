from enum import Enum
import os
import sys
import subprocess
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
        config_path = os.path.join(os.getcwd(), "custom_path.txt")
        default_windows_paths = [os.path.join(os.environ["UserProfile"], "Documents", "My Games", "Terraria")]
        default_linux_paths = ["~/.local/share/Terraria"]

        if Setup.current_pc_os == Path.WINDOWS:
            for path in default_windows_paths:
                if os.path.exists(path):
                    Setup.current_pc_rootpath = path
                    print("Default directory found")
                elif os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        Setup.current_pc_rootpath = f.readline().strip()
                    print("Custom directory found")
                else:
                    Path.pc_custom_path()
        
        elif Setup.current_pc_os == Path.LINUX:
            for path in default_linux_paths:
                if os.path.exists(path):
                    Setup.current_pc_rootpath = path
                    print("Default directory found")
                elif os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        Setup.current_pc_rootpath = f.readline().strip()
                    print("Custom directory found")
                else:
                    Path.pc_custom_path()

    @staticmethod
    def set_android_terraria_rootpath():
        default_android_path = "sdcard/Android/data/com.and.games505.TerrariaPaid"

        command = ["adb", "shell", "ls",  default_android_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print("Terraria path on android does not exist")
            print("Error:", error.decode())
        else:
            Setup.current_android_rootpath = default_android_path
        
    @staticmethod
    def pc_custom_path():
        config_path = os.path.join(os.getcwd(), "custom_path.txt")

        path = input("Default directory not found.\nYou can enter the custom path of where you have set the Terraria directory.\nExample: path/to/'Terraria'.\nPress 'q' to terminate program.\n")

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
