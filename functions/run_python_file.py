import os
import subprocess

def run_python_file(working_directory, file_path, args=[]): # directory is a relative directory relative to the working directory
    abs_working = os.path.abspath(working_directory)
    abs_current = os.path.abspath(os.path.join(working_directory, file_path))

    abs_working_sep = os.path.join(abs_working, "") # adds a trailing separator

    if not (abs_current.startswith(abs_working_sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    else: 
        if not os.path.exists(abs_current): # checks if it is actually a file
            return f'Error: File "{file_path}" not found.'
        elif file_path[-3:] != ".py":
            return f'Error: File "{file_path}" is not a Python file.'
        
        all_args = ["python", file_path] + args
        try: 
            completed_process = subprocess.run(all_args, capture_output=True, cwd=abs_working, timeout=30, check=True)
        except Exception as e:
            return f"Error: executing Python file: {e}"

        stdout = f"STDOUT: {completed_process.stdout}"
        stderr = f"STDERR: {completed_process.stderr}"
        exit_code = completed_process.returncode

        if exit_code != 0:
            exit_string = f"Process exited with code {exit_code}"
            return "\n".join([stdout, stderr, exit_string])
        
        return "\n".join([stdout, stderr])
    

