import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure target is inside working directory
        if not target_path.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Must exist and be a regular file
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Must be a Python file
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", target_path]
        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        # Non-zero exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # No output at all
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"