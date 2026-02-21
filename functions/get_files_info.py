import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    if valid_target_dir != True:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) != True:
        return f'Error: "{directory}" is not a directory'
    try:
        results = []
        for item in os.listdir(target_dir):
            full_path = os.path.join(target_dir, item)
            file_name = item
            file_size = os.path.getsize(full_path)
            true_dir = os.path.isdir(full_path)
            results.append(f"- {file_name}: file_size={file_size} bytes, is_dir={true_dir}")
        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)