import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, *args):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_directory, file_path))
        valid_target_path = os.path.commonpath([absolute_working_directory, target_path]) == absolute_working_directory
        if not valid_target_path: return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path): return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('py'): return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]
        if args: command.extend(*args)
        output_string = ""

        completed_process = subprocess.run(command, text=True,capture_output=True,timeout=30)

        if completed_process.returncode != 0: 
            output_string += f"Process exited with code {completed_process.returncode}\n"
        if completed_process.stdout == completed_process.stderr == None:
            output_string += "No output produced"
        else:
            output_string += f"STDOUT: {completed_process.stdout}"
            output_string += F"STDERR: {completed_process.stderr}\n"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python script in a specified directory relative to the working directory, returns the result",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to python script, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional set of parameters to feed to the scrpit, the items in the ARRAY must be STRINGS"
            )
        },
        required=["file_path"]
    ),
)

