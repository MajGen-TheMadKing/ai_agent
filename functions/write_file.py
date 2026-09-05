import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # gets the working directories absolute path
        working_dir_abs = os.path.abspath(working_directory)
        # creates the target path
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # validates if target_dir is inside the working_dir
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # checks if the target_file is an existing dir
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing to file: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Opens a file and writes content to it",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content that is supposed to be written to the file",
                },
            },
        },
        "required": ["file_path"],
    },
}
