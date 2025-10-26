import os

MAX_TOKENS = 10000
def get_file_content(working_directory, file_path): # directory is a relative directory relative to the working directory
    abs_working = os.path.abspath(working_directory)
    abs_current = os.path.abspath(os.path.join(working_directory, file_path))

    abs_working_sep = os.path.join(abs_working, "") # adds a trailing separator

    if not (abs_current.startswith(abs_working_sep)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    else: 
        if not os.path.isfile(abs_current): # checks if it is actually a file
            return f'Error: "{file_path}" is not a file'
        
    with open(abs_current, "r") as f:
        file_contents = f.read()
        if len(file_contents) > MAX_TOKENS:
            return f"{file_contents[:MAX_TOKENS]}...File {file_path} truncated at 10000 characters"
        return file_contents
    