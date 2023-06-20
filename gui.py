from sync import Sync
from backup import Backup
from enums import Path

def adb_pull_all(sync_object, backup_object):
    backup_object.adb_pull_so_pc_backup()
    sync_object.adb_pull_directory()

def adb_push_all(sync_object, backup_object):
    backup_object.adb_push_so_android_backup()
    sync_object.adb_push_directory()

def main():
    if Sync.check_pc_os() and Sync.check_pc_dir(Sync.check_pc_os().get_terraria_root_dir()):
        if Sync.check_adb() and Sync.check_adb_dir(Path.ANDROID.get_terraria_root_dir()):
            
            Backup.curr_pc_os = Sync.check_pc_os().value
            Backup.check_android_backup_dir()
            Backup.check_pc_backup_dir()

            Sync.curr_pc_os = Sync.check_pc_os()
            obj_player_sync = Sync(Sync.curr_pc_os.get_terraria_player_dir(), Path.ANDROID.get_terraria_player_dir())
            obj_player_sync_backup = Backup(Sync.curr_pc_os.get_terraria_player_dir(), Path.ANDROID.get_terraria_player_dir())
            
            #adb_pull_all(obj_player_sync, obj_player_sync_backup)
            #adb_push_all(obj_player_sync, obj_player_sync_backup)

            print("Complete!")

if __name__ == "__main__":
    main()