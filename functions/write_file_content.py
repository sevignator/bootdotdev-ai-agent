import os
from google.genai import types


def write_file(working_directory: str, file_path: str, content: str):
    abs_wd_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_wd_path, file_path))

    if not abs_file_path.startswith(abs_wd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'

    # Create any additional sub-directory if it doesn't already exist
    if not os.path.exists(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path))

    with open(abs_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return (
        f'Successfully wrote to "{abs_file_path}" ({len(content)} characters written).'
    )


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a provided file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write onto the file.",
            ),
        },
    ),
)
