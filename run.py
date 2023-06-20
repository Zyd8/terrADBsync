from sync import Sync
from backup import Backup
from enums import Path

obj_players_sync = Sync(Sync.check_pc_os().get_terraria_players_dir(), Path.ANDROID.get_terraria_players_dir())
obj_worlds_sync = Sync(Sync.check_pc_os().get_terraria_worlds_dir(), Path.ANDROID.get_terraria_worlds_dir())
obj_players_backup = Backup(Sync.check_pc_os().get_terraria_players_dir(), Path.ANDROID.get_terraria_players_dir())
obj_worlds_backup = Backup(Sync.check_pc_os().get_terraria_worlds_dir(), Path.ANDROID.get_terraria_worlds_dir())

def adb_pull_all(sync_object, backup_object):
    backup_object.backup_pc_files()
    sync_object.adb_pull_directory()

def adb_push_all(sync_object, backup_object):
    backup_object.backup_android_files()
    sync_object.adb_push_directory()

def main():
    # Check for existing Terraria directories
    if Sync.check_pc_os() and Sync.check_pc_dir(Sync.check_pc_os().get_terraria_root_dir()):
        if Sync.check_adb() and Sync.check_adb_dir(Path.ANDROID.get_terraria_root_dir()):
            
            # Check for existing "backups" directory, otherwise, create
            Backup.curr_pc_os = Sync.check_pc_os().value
            Backup.check_android_backup_dir()
            Backup.check_pc_backup_dir()
     
            #adb_pull_all(obj_players_sync, obj_players_backup)
            #adb_pull_all(obj_worlds_sync, obj_worlds_backup)
            #adb_push_all(obj_players_sync, obj_players_backup)
            #adb_push_all(obj_worlds_sync, obj_worlds_backup)

            print("Complete!")

if __name__ == "__main__":
    main()