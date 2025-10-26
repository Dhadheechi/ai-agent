import os
from google.genai import types

def get_files_info(working_directory, directory="."): # directory is a relative directory relative to the working directory
    abs_working = os.path.abspath(working_directory)
    abs_current = os.path.abspath(os.path.join(working_directory, directory))

    abs_working_sep = os.path.join(abs_working, "") # adds a trailing separator

    if not (abs_working == abs_current or abs_current.startswith(abs_working_sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else: 
        if not os.path.isdir(abs_current):
            return f'Error: "{directory}" is not a directory'
        
        contents_list = os.listdir(abs_current)
        info_string = []
        for name in contents_list:
            full_path = os.path.abspath(os.path.join(abs_current, name))
            is_dir = os.path.isfile(full_path)
            file_size = os.path.getsize(full_path)
            file_info = f" - {name}: file_size={file_size} bytes, is_dir={is_dir}"
            info_string.append(file_info)

        return "\n".join(info_string)
    
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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of the specified file and returns it, constrained to the working directory. If the file is longer than 10000 characters, reads only the first 10000.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the content from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file and returns it's STDOUT and STDERR, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file path to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY, 
                description="Additional arguments to run the python file", 
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A particular argument in the args array"
                )
            )
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to the specified file, constrained to the working directory. Overwrites the file with the content if it already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING, 
                description="The content (a string) that is written to the given file"
            )
        },
    ),
)


