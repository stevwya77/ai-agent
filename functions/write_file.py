import os
from google.genai import types


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    work_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(full_path)

    # check absolute path oob working directory
    if not file_abs_path.startswith(work_abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # create file path if doesn't exist
    try:
        if not os.path.exists(file_abs_path):
            with open(file_abs_path, 'w') as f:
                f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        raise Exception("Error: Could not create file")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory. If file does not exist, create file and write to it.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write in the specified file.",
            ),
        },
    ),
)