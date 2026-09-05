import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # gets the working directories absolute path
        working_dir_abs = os.path.abspath(working_directory)
        # creates the target path
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # validates if target_dir is inside the working_dir
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # checks if the target_file is an existing dir
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        # check if file is a python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'


        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_subprocess = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output_str =  ""

        if completed_subprocess.returncode != 0:
            output_str = f"Process exited with code {completed_subprocess.returncode}"
        if not completed_subprocess.stderr and not completed_subprocess.stdout:
            output_str += "\nNo output produced"
        else:
            output_str += f"\nSTDOUT: {completed_subprocess.stdout}\nSTDERR: {completed_subprocess.stderr}"

        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"
