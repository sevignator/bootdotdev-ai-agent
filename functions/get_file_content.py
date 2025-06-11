import os


def get_file_content(working_directory, file_path):
    abs_wd_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_wd_path, file_path))
    file_size = os.path.getsize(abs_file_path)
    MAX_CHAR = 10000

    if not abs_file_path.startswith(abs_wd_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(abs_file_path, "r", encoding="utf-8") as f:
        message = f.read(MAX_CHAR)

        if file_size > MAX_CHAR:
            message += f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'

    return message
