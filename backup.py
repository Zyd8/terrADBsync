import subprocess
from enums import *

class Backup:

    curr_pc_os = ""

    def check_pc_backup_dir(self):
        if Backup.curr_pc_os == Path.WINDOWS.value:
            if not os.path.exists(Path.WINDOWS.get_terraria_backup_root_dir()):

                Backup.make_pc_backup_dir(Path.WINDOWS.get_terraria_backup_root_dir())
                print("PC backup root folder is created as it does not exist")

            elif self.pc == Path.WINDOWS.get_terraria_player_dir() or self.pc == Path.WINDOWS.get_terraria_world_dir():
                if not os.path.exists(os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), self.get_pc_end_path())):

                    Backup.make_pc_backup_dir(os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), self.get_pc_end_path()))
                    print("PC backup branch folder is created as it does not exist")
            
        if Backup.curr_pc_os == Path.LINUX.value:
            if not os.path.exists(Path.LINUX.get_terraria_backup_root_dir()):

                Backup.make_pc_backup_dir(Path.LINUX.get_terraria_backup_root_dir())
                print("PC backup root folder is created as it does not exist")

            elif self.pc == Path.LINUX.get_terraria_player_dir() or self.pc == Path.LINUX.get_terraria_world_dir():
                if not os.path.exists(os.path.join(Path.LINUX.get_terraria_backup_root_dir(), self.get_pc_end_path())):

                    Backup.make_pc_backup_dir(Path.LINUX.get_terraria_backup_root_dir(), self.get_pc_end_path())
                    print("PC backup branch folder is created as it does not exist")
            
    def check_android_backup_dir(self):
        backup_root_path = os.path.join(Path.ANDROID.get_terraria_root_dir(), "backups").replace("\\", "/")
        command = ["adb", "shell", "ls", backup_root_path]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0 and not process.stdout:
            print("Android backup root folder is created as it does not exist")
            Backup.make_android_backup_dir(backup_root_path)
        else:
            backup_branch_path = os.path.join(Path.ANDROID.get_terraria_root_dir(), "backups", self.get_android_end_path()).replace("\\", "/")
            command = ["adb", "shell", "ls", backup_branch_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0 and not process.stdout:
                print("Android backup branch folder is created as it does not exist")
                Backup.make_android_backup_dir(backup_branch_path)

    @staticmethod
    def make_pc_backup_dir(directory):
        try:
            os.makedirs(directory)
            print("Folder created successfully.")
        except OSError as e:
            print(f"Failed to create folder: {e}")

    @staticmethod
    def make_android_backup_dir(directory):
        command = ["adb", "shell", "mkdir", directory]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.stdout:
            print("Output:", process.stdout)
        if process.stderr:
            print("Error:", process.stderr)