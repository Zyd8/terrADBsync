from sync import Sync
from enums import Path

def main():
    if Sync.check_pc_os() and Sync.check_pc_dir(Sync.check_pc_os().get_terraria_root_dir()):
        if Sync.check_adb() and Sync.check_adb_dir(Path.ANDROID.get_terraria_root_dir()):
            current_pc = Sync.check_pc_os()

            obj_player = Sync(current_pc.get_terraria_player_dir(), Path.ANDROID.get_terraria_player_dir())
            obj_player.adb_push_directory()
            print("Complete!")

if __name__ == "__main__":
    main()