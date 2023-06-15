from terradbsync_class import Sync_Manager
from terradbsync_enums import Path

def main():
    
    if Sync_Manager.check_pc_os() and Sync_Manager.check_pc_dir(Sync_Manager.check_pc_os().get_terraria_root_dir()):
        current_pc = Sync_Manager.check_pc_os()
        if Sync_Manager.check_adb() and Sync_Manager.check_adb_dir(Path.ANDROID.get_terraria_root_dir()):
            
            
            obj_player = Sync_Manager(current_pc.get_terraria_player_dir(), Path.ANDROID.get_terraria_player_dir())
            obj_player.adb_push_directory()
            

            print("Complete!")

if __name__ == "__main__":
    main()