from sync import Sync
from backup import Backup
from enums import Path


def check_backups():
    '''Check for existing "backups" directory, otherwise, create'''
    Backup.check_android_dir(Path.ANDROID.get_terraria_backup_rootpath())
    Backup.check_pc_dir(Backup.curr_pc_os.get_terraria_backup_rootpath())

def check_terraria_dirs():
    '''Check for existing Terraria directories, otherwise, terminate'''
    if Sync.check_pc_os() and Sync.check_pc_dir(Sync.check_pc_os().get_terraria_rootpath()):
        if Sync.check_adb_connection() and Sync.check_android_dir(Path.ANDROID.get_terraria_rootpath()):
            return True
        return False
    return False

def assign_class_global_var():
    Backup.curr_pc_os = Sync.check_pc_os()
    Sync.curr_pc_os = Sync.check_pc_os()

def main():
    if check_terraria_dirs():
        assign_class_global_var()
        check_backups()
        for android_path, pc_path in zip(Path.ANDROID.get_terraria_array_subpath(), Sync.check_pc_os().get_terraria_array_subpath()):

            #object_backup = Backup(android_path, pc_path)
            #object_backup.execute_backup()

            object_sync = Sync(android_path, pc_path)
            object_sync.execute_sync()
    
    print("TerrADBsync Complete!")

if __name__ == "__main__":
    main()