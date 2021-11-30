import os
import re


def write_to_file(content: str, output_file: str):
    with open(output_file, "w") as output_handle:
        output_handle.write(content)


def sanitize_identifier(identifier: str):
    return re.sub("[^a-zA-Z0-9_]", "_", identifier)


def map_directory_into_constants(start_dir: str):
    import_output_buffer = "import os\n"
    directory_output_buffer = "# Scanned directory names\n"
    file_output_buffer = "# Scanned file names\n"
    file_path_output_buffer = "# Scanned file paths\n"
    start_dir_basename = os.path.basename(start_dir)

    directory_output_buffer += f"ROOT_DIR = '{start_dir_basename}'\n"
    for root, dirs, files in os.walk(os.path.join(os.curdir, start_dir)):
        directory_names = set()
        for file in files:
            file_name = os.path.splitext(file)[0]
            parent_basename = os.path.basename(os.path.dirname(os.path.join(root, file)))
            dir_constant_name = sanitize_identifier(f"{start_dir_basename.upper()}_{parent_basename.upper()}_DIR")

            if parent_basename not in directory_names:
                directory_output_buffer += f"{dir_constant_name} = '{parent_basename}'\n"
                directory_names.add(parent_basename)

            file_constant_name = sanitize_identifier(f"{parent_basename.upper()}_{file_name.upper()}_FILE")
            file_output_buffer += f"{file_constant_name} = '{file}'\n"

            file_path_constant_name = sanitize_identifier(f"{parent_basename.upper()}_{file_name.upper()}_PATH")
            file_path_output_buffer += f"{file_path_constant_name} = '/'.join((" \
                                       f"{dir_constant_name}, {file_constant_name}))\n"

    return f"{import_output_buffer}\n\n{directory_output_buffer}\n{file_output_buffer}\n{file_path_output_buffer}\n"


if __name__ == "__main__":
    path_scanner_entities = [
        dict(
            start_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "static"),
            output_source_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, \
                "constants/static_constants.py")
        ),
        dict(
            start_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "templates"), 
            output_source_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, \
                "constants/template_constants.py")
        )
    ]

    for entity_dict in path_scanner_entities:
        start_dir, output_source_file = entity_dict.values()
        file_layout_text = map_directory_into_constants(start_dir)
        write_to_file(file_layout_text, output_source_file)
