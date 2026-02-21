import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.normpath(os.path.join(wd_abs, file_path)))

        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_abs), exist_ok=True)

        with open(target_abs, "w") as f:
            f.write(content)

        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes given content to a file at a specified file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of file to write to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to a specified file"     
            ),
        },
        required=["file_path", "content"],
    ),
)