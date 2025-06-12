import os


def write_file(working_directory, file_path, content):
    abs_wd_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_wd_path, file_path))

    if not abs_file_path.startswith(abs_wd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Create any additional sub-directory if it doesn't already exist
    if not os.path.exists(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path))

    with open(abs_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return (
        f'Successfully wrote to "{abs_file_path}" ({len(content)} characters written)'
    )
