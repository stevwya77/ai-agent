import os
from google.genai import types

'''
Directory parameter is treated as a relative path 
within working directory to avoid out of bounds requests.
'''


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    work_abs_path = os.path.abspath(working_directory)
    dir_abs_path = os.path.abspath(full_path)

    if not dir_abs_path.startswith(work_abs_path):
        return types.Part(function_response=types.FunctionResponse(
            name="get_files_info",
            response={"error": f"Cannot list {directory} as it is outside the permitted working directory"},
        ))

    if not os.path.isdir(dir_abs_path):
        return types.Part(function_response=types.FunctionResponse(
            name="get_files_info",
            response={"error": f'"{directory}" is not a directory'},
        ))

    entries = []
    for item in os.listdir(full_path):
        path = os.path.join(full_path, item)
        entries.append({
            "name": item,
            "file_size": os.path.getsize(path),
            "is_dir": os.path.isdir(path),
        })

    return types.Part(function_response=types.FunctionResponse(
        name="get_files_info",
        response={"directory": directory, "entries": entries},
    ))

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