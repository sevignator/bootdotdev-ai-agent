import os


def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    abs_target_directory = os.path.abspath(
        os.path.join(abs_working_directory, directory)
    )

    if not abs_target_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target_directory):
        return f'Error: "{directory}" is not a directory'

    output = ""

    for item_name in os.listdir(abs_target_directory):
        item_path = os.path.abspath(os.path.join(abs_target_directory, item_name))
        file_size = os.path.getsize(item_path)
        is_dir = os.path.isdir(item_path)

        output += f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}\n"

    return output
