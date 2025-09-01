import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a new file location, or overwrites the contents of an existing file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory. If not provided, function will return error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string containing the content to be written into the file."
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    file_loc = os.path.abspath(os.path.join(working_directory, file_path))
    directory_loc = os.path.abspath(working_directory)

    if os.path.commonpath((file_loc, directory_loc)) != directory_loc:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    file_directory = os.path.dirname(file_loc)

    try:
        if not os.path.exists(file_directory):
            os.makedirs(file_directory)
        
        with open(file_loc, "w") as f:
            f.write(content)

    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'