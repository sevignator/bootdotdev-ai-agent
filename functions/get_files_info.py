import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    abs_wd_path = os.path.abspath(working_directory)
    abs_dir_path = os.path.abspath(os.path.join(abs_wd_path, directory))

    if not abs_dir_path.startswith(abs_wd_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_dir_path):
        return f'Error: "{directory}" is not a directory'

    output = ""

    for item_name in os.listdir(abs_dir_path):
        item_path = os.path.abspath(os.path.join(abs_dir_path, item_name))
        file_size = os.path.getsize(item_path)
        is_dir = os.path.isdir(item_path)

        output += f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}\n"

    return output


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
