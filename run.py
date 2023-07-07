from path import Path
from setup import Setup
from sync import Sync
from backup import Backup

def set_backups():
    """makes "backups" directory if not created, else, create"""
    Backup.set_android_dir(Path.ANDROID.get_terraria_backup_rootpath())
    Backup.set_pc_dir(Backup.current_pc_os.get_terraria_backup_rootpath())

def set_pc_android():
    """Identify PC os and initialize adb connection"""
    Sync.check_pc_os()
    Sync.check_adb_connection()

def set_paths():
    """Find default Terraria directories, else, initialize custom paths"""
    Path.set_pc_terraria_rootpath()
    Path.set_android_terraria_rootpath()

def main():

    set_pc_android()
    set_paths()
    set_backups()

    for android_path, pc_path in zip(Path.ANDROID.get_terraria_array_subpath(), Setup.current_pc_os.get_terraria_array_subpath()):

        object_backup = Backup(android_path, pc_path)
        object_backup.execute_backup()
        object_sync = Sync(android_path, pc_path)
        object_sync.execute_sync()
    
    print("TerrADBsync Complete!")

if __name__ == "__main__":
    main()