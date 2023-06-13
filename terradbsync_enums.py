from enum import Enum
import os

class Operating_System(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    ANDROID = "Android"

            
    def get_terraria_root_dir(self):
        if self == Operating_System.WINDOWS:
            return os.path.join(os.environ["UserProfile"], "Documents", "My Games", "Terraria")
        elif self == Operating_System.LINUX:
            return "~/.local/share/Terraria"
        elif self == Operating_System.ANDROID:
            return "sdcard/Android/data/com.and.games505.TerrariaPaid"
        
    def get_terraria_player_dir(self):
        if self == Operating_System.WINDOWS:
            return os.path.join(os.environ["UserProfile"], "Documents", "My Games", "Terraria", "Players")
        elif self == Operating_System.LINUX:
            return "~/.local/share/Terraria/Players"
        elif self == Operating_System.ANDROID:
            return "sdcard/Android/data/com.and.games505.TerrariaPaid/Players"

    def get_terraria_world_dir(self):
        if self == Operating_System.WINDOWS:
            return os.path.join(os.environ["UserProfile"], "Documents", "My Games", "Terraria", "Worlds")
        elif self == Operating_System.LINUX:
            return "~/.local/share/Terraria/Worlds"
        elif self == Operating_System.ANDROID:
            return "sdcard/Android/data/com.and.games505.TerrariaPaid/Worlds"