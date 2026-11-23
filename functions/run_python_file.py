import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        elif not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args is not None:
            command.extend(args)

        run_file = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        output_string = []
        if run_file.returncode != 0:
            output_string.append(f'Process exited with code {run_file.returncode}')

        if len(run_file.stdout) == 0 and len(run_file.stderr) == 0:
            output_string.append("No output produced")

        if len(run_file.stdout) != 0:
            output_string.append(f'STDOUT:{run_file.stdout}')

        if len(run_file.stderr) != 0:
            output_string.append(f'STDERR:{run_file.stderr}')

        return "\n".join(output_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file relative to the working directory with optional command-line arguments, and returns its stdout, stderr and exit code. Times out after 30 seconds",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the .py file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the script",
                },
            },
            "required": ["file_path"],
        },
    },
}
