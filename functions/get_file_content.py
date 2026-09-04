from config import MAX_READ_LENGTH
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # gets the working directories absolute path
        working_dir_abs = os.path.abspath(working_directory)
        # creates the target path
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # validates if target_dir is inside the working_dir
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # checks if the file_path actualy leads to a file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content = f.read(MAX_READ_LENGTH)

            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_READ_LENGTH} characters]'
        return file_content

    except Exception as e:
        return f"Error getting contents of file: {e}"
