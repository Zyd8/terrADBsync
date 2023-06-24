from enum import Enum
import os

class Path(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    ANDROID = "Android"

    def get_terraria_rootpath(self):
        if self == Path.WINDOWS:
            return os.path.join(os.environ["UserProfile"], "Documents", "My Games", "Terraria")
        elif self == Path.LINUX:
            return "~/.local/share/Terraria"
        elif self == Path.ANDROID:
            return "sdcard/Android/data/com.and.games505.TerrariaPaid"
        
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