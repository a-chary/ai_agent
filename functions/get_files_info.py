import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    rel_path = os.path.join(working_directory, directory)
    full_dir_path = os.path.abspath(rel_path)
    full_working_path = os.path.abspath(working_directory)

    if os.path.commonpath((full_dir_path, full_working_path)) != full_working_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_dir_path):
        return f'Error: "{directory}" is not a directory'

    file_list = os.listdir(full_dir_path)
    contents_dir = ''
    for file in file_list:
        file_path = os.path.join(full_dir_path, file)
        try:
            is_dir = os.path.isdir(file_path)
            size = os.path.getsize(file_path)
        except Exception as e:
            return f"Error: {e}"
        contents_dir += " - " + file + ": file_size=" + str(size) + " bytes, is_dir=" + str(is_dir) + "\n"
    return contents_dir