import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure target is inside working directory
        if not target_path.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it exists and is a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_CHARS
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

            # Check if file was truncated
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"