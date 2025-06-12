import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_wd_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_wd_path, file_path))

    if not abs_file_path.startswith(abs_wd_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        message = ""

        completed_process = subprocess.run(
            ["python3", file_path],
            check=False,
            cwd=abs_wd_path,
            timeout=30,
            capture_output=True,
        )

        if completed_process.stdout:
            message += f"STDOUT: {completed_process.stdout.decode("utf-8")}\n"

        if completed_process.stderr:
            message += f"STDERR: {completed_process.stderr.decode("utf-8")}\n"

        if completed_process.returncode != 0:
            message += f"Process exited with code {completed_process.returncode}\n"

        if len(message) == 0:
            message = "No output produced.\n"

        return message

    except Exception as e:
        return f"Error: executing Python file: {e}"
