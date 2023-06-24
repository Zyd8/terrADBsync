
    # should be handle_android_backup_dir()

# MIGHT BE UNNNESCESASAASASRYYY
"""
        elif Sync.curr_pc_os == Path.LINUX.value:
                file_list = os.listdir(self.pc_dir)
                for file in file_list:
                    filename, extension = os.path.splitext(file)
                    if not Sync.is_valid_extension(extension):
                        continue
                    file_path = os.path.join(self.pc_dir, file)
                    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    last_modified = last_modified.strftime("%Y-%m-%d %H:%M:%S")

                    pc_path_date_dict = {}
                    pc_path_date_dict["file_path"] = file_path
                    pc_path_date_dict["last_modified"] = last_modified
                    pc_path_date_list.append(pc_path_date_dict)
"""