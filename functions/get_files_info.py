import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # gets the working directories absolute path
        working_dir_abs = os.path.abspath(working_directory)
        # creates the target path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # validates if target_dir is inside the working_dir
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

         # validates if the directory given is actualy a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_info: list[str] = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)

    except Exception as e:
        print(f"Error listing files: {e}")

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
