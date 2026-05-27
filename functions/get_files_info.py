import os

def get_path(target_dir, file):
    return os.path.normpath(os.path.join(target_dir, file))

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_directory, directory))
        valid_target_dir = os.path.commonpath([absolute_working_directory, target_dir]) == absolute_working_directory
        if not os.path.isdir(target_dir): return f'Error: "{directory}" is not a directory'
        if not valid_target_dir: return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        print(f'Success: "{directory}" is within the working directory\n')
        
        files = os.listdir(target_dir)
        listofiles = []

        for file in files:
            string = f'- {file}: file_size={os.path.getsize(get_path(target_dir, file))}, is_dir={os.path.isdir(get_path(target_dir, file))}'
            listofiles.append(string)
        
        return "\n".join(listofiles) + "\n"
    except Exception as e:
        return f'Error: Something went amiss, {e}'

