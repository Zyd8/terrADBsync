import datetime
import hashlib
import os
import subprocess
import tempfile

from errorhandler import ErrorHandler
from path import Path
from setup import Setup


class Sync(Setup):


    def __init__(self, android_path, pc_path):
        self.android_path = android_path
        self.pc_path = pc_path


    @staticmethod
    @ErrorHandler.handle_error
    def check_adb_connection():
        """Establish connection with the android device"""
        output = subprocess.check_output([Setup.adb_path,"devices"]).decode()
        lines = output.strip().split('\n')
        if len(lines) > 1:
            devices = lines[1:]
            for device in devices:
                if "device" in device:
                    continue
        else:
            raise RuntimeError("Android device cannot be found through adb connection")
        
    
    @staticmethod
    @ErrorHandler.handle_error
    def check_adb_dir():
        """Check if the required sdk is present"""
        if Setup.current_pc_os == Path.WINDOWS:
            adb_path = os.path.join(os.getcwd(), "adb_sdk", "windows", "adb.exe")
        elif Setup.current_pc_os == Path.LINUX:
            adb_path =  os.path.join(os.getcwd(), "adb_sdk", "linux", "adb")
        Setup.check_pc_dir(adb_path)
        Setup.adb_path = adb_path
   

    @staticmethod
    @ErrorHandler.handle_error
    def check_pc_os():
        """Identify the PC os"""
        if os.name == "posix":
            Setup.current_pc_os = Path.LINUX
        elif os.name == "nt":
            Setup.current_pc_os = Path.WINDOWS
        else:
            print("The PC operating system is not supported")
            Sync.with_error_terminate()
    

    @staticmethod
    @ErrorHandler.handle_error
    def compare_dates(android_path_date_list, pc_path_date_list):
        """Compare the file paths and modification dates to determine the files to be synced"""
        copy_to_android = []
        copy_to_pc = []

        for android_file in android_path_date_list:
            android_path = android_file["file_path"]
            android_date = android_file["last_modified"]
            android_filename = os.path.basename(android_path)

            for pc_file in pc_path_date_list:
                pc_path = pc_file["file_path"]
                pc_date = pc_file["last_modified"]
                pc_filename = os.path.basename(pc_path)

                if android_filename == pc_filename:
                    android_temp_path = Sync.set_android_tempfile(android_path)
                    if Sync.get_md5(android_temp_path) != Sync.get_md5(pc_path):
                        if pc_date > android_date:
                            copy_to_android.append(pc_path)
                        elif pc_date < android_date:
                            copy_to_pc.append(android_path)
                    os.remove(android_temp_path)

        for android_path_date in android_path_date_list:
            android_path = android_path_date["file_path"]
            android_filename = os.path.basename(android_path)
            if not any(android_filename == os.path.basename(entry["file_path"]) for entry in pc_path_date_list):
                print(f"A new file is being synced from android: {os.path.basename(android_path)}")
                copy_to_pc.append(android_path)

        for pc_path_date in pc_path_date_list:
            pc_path = pc_path_date["file_path"]
            pc_filename = os.path.basename(pc_path)
            if not any(pc_filename == os.path.basename(entry["file_path"]) for entry in android_path_date_list):
                print(f"A new file is being synced from pc: {os.path.basename(pc_path)}")
                copy_to_android.append(pc_path)

        return copy_to_android, copy_to_pc
    

    @staticmethod
    @ErrorHandler.handle_error
    def get_md5(path):
        """Reads the md5 hash of a file"""
        md5_hash = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()
    

    @staticmethod
    @ErrorHandler.handle_error
    def pull_files_from_android(path_list):
        """Transfer files from android to PC"""
        for path in path_list:
            source_path = path
            destination_path = os.path.join(Sync.current_pc_rootpath, os.path.basename(os.path.dirname(source_path)))
            process = Setup.do_adb(["pull", source_path, destination_path])
            if process.stdout:
                print("Sync:", process.stdout, end="")
        

    @staticmethod
    @ErrorHandler.handle_error
    def push_files_to_android(path_list):
        """Transfer files from PC to android"""
        for path in path_list:
            source_path = path
            destination_path = os.path.join(Sync.current_android_rootpath,  os.path.basename(os.path.dirname(source_path))).replace("\\", "/")
            process = Setup.do_adb(["push", source_path, destination_path])
            if process.stdout:
                print("Sync:", process.stdout, end="")


    @staticmethod
    @ErrorHandler.handle_error
    def set_android_tempfile(path):
        """Copy temporary android files to the PC filesystem"""
        source_path = path
        destination_path = os.path.join(tempfile.gettempdir(), os.path.basename(path))
        Setup.do_adb(["pull", source_path, destination_path])

        return destination_path
    

    def execute_sync(self):
        android_path_date_list, pc_path_date_list = Sync.get_modified_dates(self) 
        copy_to_android, copy_to_pc = Sync.compare_dates(android_path_date_list, pc_path_date_list)
        Sync.push_files_to_android(copy_to_android)
        Sync.pull_files_from_android(copy_to_pc)


    @ErrorHandler.handle_error
    def get_modified_dates(self):
        """Extract the file paths and its last modified dates, placing the pair in a dictionary, then to a list"""
        # Android side
        android_path_date_list = []
        process = Setup.do_adb(["shell", "ls", self.android_path])
        file_list = process.stdout.splitlines()
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if not Setup.is_valid_extension(extension):
                continue
            file_path =  os.path.join(self.android_path, file).replace("\\", "/")
            process = Setup.do_adb(["shell", "stat", "-c", "%y", file_path])
            output = process.stdout.strip()
            last_modified = datetime.datetime.strptime(output[:19], "%Y-%m-%d %H:%M:%S")
            last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")
            android_path_date_dict = {}
            android_path_date_dict["file_path"] = file_path
            android_path_date_dict["last_modified"] = last_modified
            android_path_date_list.append(android_path_date_dict)
        # PC side
        pc_path_date_list = []
        file_list = os.listdir(self.pc_path)
        for file in file_list:
            filename, extension = os.path.splitext(file)
            if not Setup.is_valid_extension(extension):
                continue
            file_path = os.path.join(self.pc_path, file)
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")
            pc_path_date_dict = {}
            pc_path_date_dict["file_path"] = file_path
            pc_path_date_dict["last_modified"] = last_modified
            pc_path_date_list.append(pc_path_date_dict)
    
        return android_path_date_list, pc_path_date_list
        
    
    