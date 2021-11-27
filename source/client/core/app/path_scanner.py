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

    for root, dirs, files in os.walk(os.path.join(os.curdir, start_dir)):
        directory_names = set()
        for file in files:
            file_name = os.path.splitext(file)[0]
            parent_basename = os.path.basename(os.path.dirname(os.path.join(root, file)))
            dir_constant_name = sanitize_identifier(f"{start_dir.upper()}_{parent_basename.upper()}_DIR")

            if parent_basename not in directory_names:
                directory_output_buffer += f"{dir_constant_name} = '{parent_basename}'\n"
                directory_names.add(parent_basename)

            file_constant_name = sanitize_identifier(f"{parent_basename.upper()}_{file_name.upper()}_FILE")
            file_output_buffer += f"{file_constant_name} = '{file}'\n"

            file_path_constant_name = sanitize_identifier(f"{parent_basename.upper()}_{file_name.upper()}_PATH")
            file_path_output_buffer += f"{file_path_constant_name} = '/'.join((os.curdir, " \
                                       f"{dir_constant_name}, {file_constant_name}))\n"

    return f"{import_output_buffer}\n\n{directory_output_buffer}\n{file_output_buffer}\n{file_path_output_buffer}\n"


if __name__ == "__main__":
    path_scanner_entities = [
        ("static", "constants/static_constants.py"),
        ("templates", "constants/template_constants.py")
    ]

    for start_dir, output_source_file in path_scanner_entities:
        file_layout_text = map_directory_into_constants(start_dir)
        write_to_file(file_layout_text, output_source_file)
