from sync import Sync
from backup import Backup
from enums import Path


def check_backups():
    '''Check for existing "backups" directory, otherwise, create'''
    Backup.curr_pc_os = Sync.check_pc_os()
    Backup.check_android_backup_dir(Path.ANDROID.get_terraria_backup_root_dir())
    Backup.check_pc_backup_dir(Backup.curr_pc_os.get_terraria_backup_root_dir())

def check_terraria_dirs():
    '''Check for existing Terraria directories, otherwise, terminate'''
    if Sync.check_pc_os() and Sync.check_pc_dir(Sync.check_pc_os().get_terraria_root_dir()):
        if Sync.check_adb_connection() and Sync.check_adb_dir(Path.ANDROID.get_terraria_root_dir()):
            return True
        return False
    return False

def main():
    if check_terraria_dirs():
        check_backups()
        for android_dir, pc_dir in zip(Path.ANDROID.get_terraria_array_dir(), Sync.check_pc_os().get_terraria_array_dir()):

            object_backup = Backup(android_dir, pc_dir)
            object_backup.execute_backup()

            object_sync = Sync(android_dir, pc_dir)
            object_sync.execute_sync()
    
    print("TerrADBsync Complete!")

if __name__ == "__main__":
    main()