
from path import Path
from sync import Sync
from backup import Backup
from setup import Setup


def do_backups():
    '''Check for existing "backups" directory, otherwise, create'''
    Backup.check_android_dir(Path.ANDROID.get_terraria_backup_rootpath())
    Backup.check_pc_dir(Backup.current_pc_os.get_terraria_backup_rootpath())

def check_terraria_dirs():
    '''Check for Terraria root directories, starting from default paths, customized or terminate'''
    Sync.check_pc_os()
    Sync.check_adb_connection()
    Path.set_pc_terraria_rootpath()
    Path.set_android_terraria_rootpath()

def main():

    check_terraria_dirs()
    do_backups()

    for android_path, pc_path in zip(Path.ANDROID.get_terraria_array_subpath(), Setup.current_pc_os.get_terraria_array_subpath()):

        object_backup = Backup(android_path, pc_path)
        object_backup.execute_backup()
        object_sync = Sync(android_path, pc_path)
        object_sync.execute_sync()
    
    print("TerrADBsync Complete!")

if __name__ == "__main__":
    main()