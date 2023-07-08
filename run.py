from path import Path
from setup import Setup
from sync import Sync
from backup import Backup

def set_backups():
    """make "backups" directory if not already created, else, create"""
    Backup.set_android_dir(Path.ANDROID.get_terraria_backup_rootpath())
    Backup.set_pc_dir(Backup.current_pc_os.get_terraria_backup_rootpath())

def set_pc_android():
    """Identify PC os and initialize adb connection"""
    Sync.check_pc_os()
    Sync.check_adb_connection()

def set_rootpaths():
    """Find default Terraria directories, else, initialize custom paths"""
    Path.set_pc_terraria_rootpath()
    Path.set_android_terraria_rootpath()

def check_subpaths():
    """Check subpaths that are supposed to exist, else, terminate program"""
    for android_path, pc_path in zip(Path.ANDROID.get_terraria_array_subpath(), Setup.current_pc_os.get_terraria_array_subpath()):
        Setup.check_android_dir(android_path)
        Setup.check_pc_dir(pc_path)

def do_backup_sync():  
    """Do main operation"""
    for android_path, pc_path in zip(Path.ANDROID.get_terraria_array_subpath(), Setup.current_pc_os.get_terraria_array_subpath()):
        obj_backup = Backup(android_path, pc_path)
        obj_backup.execute_backup()
        obj_sync = Sync(android_path, pc_path)
        obj_sync.execute_sync()

def main():
    set_pc_android()
    set_rootpaths()
    check_subpaths()
    set_backups()
    do_backup_sync()
    print("TerrADBsync Complete!")

if __name__ == "__main__":
    main()


