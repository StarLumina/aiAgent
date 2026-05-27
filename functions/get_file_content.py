import os
from config import *

def get_file_content(working_directory, file_path):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        valid_target_file = os.path.commonpath([absolute_working_directory, target_file]) == absolute_working_directory
        if not os.path.isfile(target_file): return f'Error: File not found or is not a regular file: "{file_path}"'
        if not valid_target_file: return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        content = open(target_file).read(MAX_CHARS)

        if open(target_file).read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    
    except Exception as e:
        return f'Error: Something went amiss, {e}'