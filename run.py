from sync import Sync
from backup import Backup
from enums import Path, Adb

def perform_players_sync(signal):
    obj_players_backup = Backup(Sync.check_pc_os().get_terraria_players_dir(), Path.ANDROID.get_terraria_players_dir())
    obj_players_sync = Sync(Sync.check_pc_os().get_terraria_players_dir(), Path.ANDROID.get_terraria_players_dir())
    if signal == Adb.PUSH:
        obj_players_backup.backup_android_files()
        obj_players_sync.man_push_files_to_android()
    elif signal == Adb.PULL:
        obj_players_backup.backup_pc_files()
        obj_players_sync.man_pull_files_from_android()
                
def perform_worlds_sync(signal):
    obj_worlds_backup = Backup(Sync.check_pc_os().get_terraria_worlds_dir(), Path.ANDROID.get_terraria_worlds_dir())
    obj_worlds_sync = Sync(Sync.check_pc_os().get_terraria_worlds_dir(), Path.ANDROID.get_terraria_worlds_dir())
    if signal == Adb.PUSH:
        obj_worlds_backup.backup_android_files()
        obj_worlds_sync.man_push_files_to_android()
    elif signal == Adb.PULL:
        obj_worlds_backup.backup_pc_files()
        obj_worlds_sync.man_pull_files_from_android()
        
def perform_all_sync(signal):
    perform_players_sync(signal)
    perform_worlds_sync(signal)

def main():
    '''Check for existing Terraria directories'''
    if Sync.check_pc_os() and Sync.check_pc_dir(Sync.check_pc_os().get_terraria_root_dir()):
        if Sync.check_adb_connection() and Sync.check_adb_dir(Path.ANDROID.get_terraria_root_dir()):
            
            '''Check for existing "backups" directory, otherwise, create'''
            Backup.curr_pc_os = Sync.check_pc_os().value
            Backup.check_android_backup_dir()
            # should be handle_android_backup_dir()
            Backup.check_pc_backup_dir()
            
            sync_operation = input("Manual or Auto [m/a]: ")

            if sync_operation.lower() == "a":
                Sync.perform_auto_sync()
            
            elif sync_operation.lower() == "m":

                platform_sync = input(f"Sync from {Sync.check_pc_os} to android or sync from android to {Sync.check_pc_os} [p2a/a2p]: ")
                dir_sync = input("Sync Players, Worlds, or both directory [p/w/b]: ")

                if platform_sync == "p2a" and dir_sync.lower() == "p":
                    perform_players_sync(Adb.PUSH)
                
                elif platform_sync == "a2p" and dir_sync.lower() == "p":
                    perform_players_sync(Adb.PULL)

                elif platform_sync == "p2a" and dir_sync.lower() == "w":
                    perform_worlds_sync(Adb.PUSH)

                elif platform_sync == "a2p" and dir_sync.lower() == "w":
                    perform_worlds_sync(Adb.PULL)

                elif platform_sync == "p2a" and dir_sync.lower() == "b":
                    perform_all_sync(Adb.PUSH)

                elif platform_sync == "a2p" and dir_sync.lower() == "b":
                    perform_all_sync(Adb.PULL)
                
                else:
                    print("Invalid input.")
            
            print("TerrADBsync Complete!")

            # JUST MAKE THE AUTO SYNC OPERATIONS BY DOING A FOR LOOP OF ALL THE
            # PATH ENUMS AND FEEDING IT TO THE OLD ADB PUSH/PULL, BUT NO INTEGRATED
            # WITH THE SMART OVERWRITE METHODS

if __name__ == "__main__":
    main()