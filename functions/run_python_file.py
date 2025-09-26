import os
import sys
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    work_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(full_path)

    # check absolute path oob working directory
    if not file_abs_path.startswith(work_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # check if exists
    if not os.path.exists(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    
    # file must be .py type
    if not file_abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    # use subprocess.run function, set timeout 30s, capture stdout & stderr, set workingdir, pass addtional args provided
    output = subprocess.run([sys.executable, file_abs_path, *args], cwd=work_abs_path, text=True, capture_output=True, timeout=30)
    message = ""
    if output.stdout:
        message += output.stdout
    if output.stderr:
        if message and not message.endswith("\n"):
            message += "\n"
        message += output.stderr
    return f"Command Output\n{message}" if message else "No output produced"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute specified python files with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, relative to the working directory. If argument provided, execute arguments with file.",
            ),
        },
    ),
)