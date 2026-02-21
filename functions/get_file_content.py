import os
import config
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))
        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_abs, "r") as f:
            file_content_string = f.read(config.MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of file to read",
            ),
        },
        required=["file_path"],
    ),
)