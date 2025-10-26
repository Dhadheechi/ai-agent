import os

def write_file(working_directory, file_path, content): # the function's scope is limited to the specified working directory
    abs_working = os.path.abspath(working_directory)
    abs_current = os.path.abspath(os.path.join(working_directory, file_path))

    abs_working_sep = os.path.join(abs_working, "") # adds a trailing separator

    if not (abs_current.startswith(abs_working_sep)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    else: 
        if not os.path.exists(abs_current): # checks if it is actually a file, if not, creates it
            os.makedirs(os.path.dirname(abs_current), exist_ok=True) # make the parent directory of the file we're writing to
        with open(abs_current, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path} ({len(content)} characters written)"

        
        
    