import os
from config import *
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get contents from, relative to the working directory. If not provided, function will return error.",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    file_loc = os.path.abspath(os.path.join(working_directory, file_path))
    directory_loc = os.path.abspath(working_directory)

    if os.path.commonpath((file_loc, directory_loc)) != directory_loc:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_loc):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(file_loc, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"
    
    return file_content_string