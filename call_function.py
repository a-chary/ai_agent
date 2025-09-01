from config import *
from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

FUNC_DIC = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name


    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    keyword_args = function_call_part.args.copy()
    keyword_args["working_directory"] = WORKING_DIRECTORY

    if function_name in FUNC_DIC:
        function = FUNC_DIC[function_name]
    else:
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
                )   
            ],
        )

    function_output = function(**keyword_args)
        
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_output},
            )
        ],
    )
