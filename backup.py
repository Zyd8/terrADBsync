import subprocess
from enums import *

class Backup:

    curr_pc_os = ""

    def __init__(self, pc, android):
        self.pc = pc
        self.android = android 

    def get_pc_end_path(self):
        slash_list = []
        for index, slash in enumerate(self.pc):
            if slash == "\\":
                slash_list.append(index)
        return self.pc[max(slash_list)+1::]
        
    def get_android_end_path(self):
        slash_list = []
        for index, slash in enumerate(self.android):
            if slash == "/":
                slash_list.append(index)
        return self.android[max(slash_list)+1::]

    def adb_pull_so_pc_backup(self):
        file_list = os.listdir(self.pc)
        for file in file_list:
            if Backup.curr_pc_os == Path.WINDOWS.value:
                source_path = os.path.join(self.pc, file)
                destination_path = os.path.join(Path.WINDOWS.get_terraria_backup_root_dir(), self.get_pc_end_path(), file)
                os.rename(source_path, destination_path)
            elif Backup.curr_pc_os == Path.LINUX.value:
                source_path = os.path.join(self.pc, file)
                destination_path = os.path.join(Path.LINUX.get_terraria_backup_root_dir(), self.get_pc_end_path(), file)
                os.rename(source_path, destination_path)

    def adb_push_so_android_backup(self):
        command = ["adb", "shell", "ls", self.android]
        process = subprocess.run(command, capture_output=True, text=True)
        file_list = process.stdout.splitlines()
        for file in file_list:
            source_path = os.path.join(self.android, file).replace("\\", "/")
            destination_path = os.path.join(Path.ANDROID.get_terraria_backup_root_dir(), self.get_pc_end_path(), file).replace("\\", "/")
            command = ["adb", "shell", "mv", source_path, destination_path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.stdout:
                print("Output:", process.stdout)
            if process.stderr:
                print("Error:", process.stderr)

    @staticmethod
    def check_pc_backup_dir():
        if Backup.curr_pc_os == Path.WINDOWS.value:
            for path in Path.WINDOWS.get_terraria_backup_array_dir():
                if not os.path.exists(path):
                    Backup.make_pc_backup_dir(path)
                    print(f"PC backup: {path} folder is created")

        if Backup.curr_pc_os == Path.LINUX.value:
            for path in Path.LINUX.get_terraria_backup_array_dir():
                if not os.path.exists(path):
                    Backup.make_pc_backup_dir(path)
                    print(f"PC backup: {path} folder is created")
            
    @staticmethod
    def check_android_backup_dir():
        for path in Path.ANDROID.get_terraria_backup_array_dir():
            command = ["adb", "shell", "ls", path]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0 and not process.stdout:
                print(f"Android backup: {path} folder is created")
                Backup.make_android_backup_dir(path)

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