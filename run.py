from sync import Sync
from backup import Backup
from enums import Path, Adb_Signal

def manual_players_sync(signal):
    obj_players_backup = Backup(Sync.check_pc_os().get_terraria_players_dir(), Path.ANDROID.get_terraria_players_dir())
    obj_players_sync = Sync(Sync.check_pc_os().get_terraria_players_dir(), Path.ANDROID.get_terraria_players_dir())
    if signal == Adb_Signal.PUSH:
        obj_players_backup.backup_android_files()
        obj_players_sync.manual_push_files()
    elif signal == Adb_Signal.PULL:
        obj_players_backup.backup_pc_files()
        obj_players_sync.manual_pull_files()
                
def manual_worlds_sync(signal):
    obj_worlds_backup = Backup(Sync.check_pc_os().get_terraria_worlds_dir(), Path.ANDROID.get_terraria_worlds_dir())
    obj_worlds_sync = Sync(Sync.check_pc_os().get_terraria_worlds_dir(), Path.ANDROID.get_terraria_worlds_dir())
    if signal == Adb_Signal.PUSH:
        obj_worlds_backup.backup_android_files()
        obj_worlds_sync.manual_push_files()
    elif signal == Adb_Signal.PULL:
        obj_worlds_backup.backup_pc_files()
        obj_worlds_sync.manual_pull_files()
        
def manual_all_sync(signal):
    manual_players_sync(signal)
    manual_worlds_sync(signal)

def main():
    # Check for existing Terraria directories
    if Sync.check_pc_os() and Sync.check_pc_dir(Sync.check_pc_os().get_terraria_root_dir()):
        if Sync.check_adb() and Sync.check_adb_dir(Path.ANDROID.get_terraria_root_dir()):
            
            # Check for existing "backups" directory, otherwise, create
            Backup.curr_pc_os = Sync.check_pc_os().value
            Backup.check_android_backup_dir()
            Backup.check_pc_backup_dir()


            # Will make an algorithm that will put both platforms in separate list
            # each platform's directory will find each other's pair, the rest are just copied over
            # which then each file will be compared based on the last modification date
            # after which the latest date will be chosen and the older will be overwritten
     
            #adb_pull_all(obj_players_sync, obj_players_backup)
            #adb_pull_all(obj_worlds_sync, obj_worlds_backup)
            #adb_push_all(obj_players_sync, obj_players_backup)
            #adb_push_all(obj_worlds_sync, obj_worlds_backup)

            Sync.adb_auto_sync()
            print("TerrADBsync Complete!")

if __name__ == "__main__":
    main()