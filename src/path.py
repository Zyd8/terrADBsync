from enum import Enum
import os

from src.errorhandler import ErrorHandler 
from src.setup import Setup


class Path(Enum):


    WINDOWS = "Windows"
    LINUX = "Linux"
    ANDROID = "Android"


    def get_terraria_rootpath(self):
        "Defined depending on the PC os and Terraia default/custom path"
        if self == Path.WINDOWS or self == Path.LINUX:
            return Setup.current_pc_rootpath
        elif self == Path.ANDROID:
            return Setup.current_android_rootpath
        

    def get_terraria_array_subpath(self):
        "Defined by the get_terraria_rootpath(), appending 'Players' and 'Worlds'"
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
        "Defined by the get_terraria_rootpath(), appending 'backups'"
        if self == Path.WINDOWS:
            return os.path.join(Path.WINDOWS.get_terraria_rootpath(), "backups")
        elif self == Path.LINUX:
            return f"{Path.LINUX.get_terraria_rootpath()}/backups"
        elif self == Path.ANDROID:
            return f"{Path.ANDROID.get_terraria_rootpath()}/backups"
        
        
    @staticmethod
    @ErrorHandler.handle_error
    def pc_custom_path():
        """Inquire for a Terraria rootpath"""
        print(os.getcwd())
        config_path = os.path.join(os.getcwd(), "custom_path.txt")
        path = input("Terraria directory not found in PC.\nYou can enter the custom path of where you have set the Terraria directory.\nExample: path/to/'Terraria'.\nPress 'q' to terminate program.\n")
        if path.lower() == "q":
            ErrorHandler.no_error_terminate()
        elif os.path.basename(path) != "Terraria":
            print("The inputted path must end with 'Terraria'. Try again.")
            Path.pc_custom_path()
        else: 
            if os.path.exists(path):
                print("Custom directory found")
                with open(config_path, "w") as f:
                    f.write(path)
                Setup.current_pc_rootpath = path
                print("Custom directory remembered")
            else: 
                print("Input path not found. Try again.")
                Path.pc_custom_path()
    

    @staticmethod
    @ErrorHandler.handle_error
    def set_android_terraria_rootpath():
        """Check android default Terarria rootpath, else, terminate"""
        default_path = "sdcard/Android/data/com.and.games505.TerrariaPaid"
        Setup.do_adb(["shell", "ls",  default_path])
        Setup.current_android_rootpath = default_path


    @staticmethod
    @ErrorHandler.handle_error
    def set_pc_terraria_rootpath():
        """Check PC default Terraria rootpaths then custom paths configuration file, else, prompt for a custom path"""
        config_path = os.path.join(os.getcwd(), "custom_path.txt")
        found_path = False
        
        if Setup.current_pc_os == Path.WINDOWS:
            default_paths = [os.path.join(os.environ["UserProfile"], "Documents", "My Games", "Terraria")]
        elif Setup.current_pc_os == Path.LINUX:
            default_paths = [os.path.expanduser("~/.local/share/Terraria"),
                             os.path.expanduser("~/.var/app/com.valvesoftware.Steam/.local/share/Terraria")]
        
        # Default path condition
        for path in default_paths:
            if os.path.exists(path):
                Setup.current_pc_rootpath = path
                print("Default directory found")
                found_path = True
                break
        
        # Custom path condition
        if not found_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                custom_path = f.readline().strip()
                if os.path.exists(custom_path):
                    Setup.current_pc_rootpath = custom_path
                    print("Custom directory found")
                    found_path = True

        # Custom path creation condition
        if not found_path:
            Path.pc_custom_path()