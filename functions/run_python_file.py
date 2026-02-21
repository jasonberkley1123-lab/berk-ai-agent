import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))

        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_abs) != True:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith(".py") != True:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_abs]
        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=wd_abs, capture_output=True, text=True, timeout=30)
        
        lines = []

        if result.returncode != 0:
            lines.append(f"Process exited with code {result.returncode}")
        if not result.stdout.strip() and not result.stderr.strip():
            lines.append("No output produced")
        else:
            if result.stdout.strip():
                lines.append(f"STDOUT: {result.stdout}")
            if result.stderr.strip():
                lines.append(f"STDERR: {result.stderr}")
        
        return "\n".join(lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file with any given arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of a specified python file to be ran",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Arguments to be used in a python file"
            )
        },
        required=["file_path"]
    ),
)