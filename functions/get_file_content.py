import os
from google.genai import types


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(full_path)
    abs_work = os.path.abspath(working_directory)

    # check if outside working directory
    if not abs_file.startswith(abs_work):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
   
    # check if not a file
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # read file
    try: 
        with open(full_path, 'r') as f:
            contents = f.read()
    except:
        raise Exception("Error: Could not read file")
    
    # truncate and append message if longer than 10000 chars
    try: 
        if len(contents) > 10000:
            return f'{contents[:10000]}[...File "{file_path}" truncated at 10000 characters]'
        else:
            return contents
    except:
        raise Exception("Error: Could not print file contents")
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read contents of the specified file and return up to first 1000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read content from, relative to the working directory.",
            ),
        },
    ),
)