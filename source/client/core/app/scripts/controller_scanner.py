import re
import os

def write_to_file(content: str, output_file: str):
    with open(output_file, "w") as output_handle:
        output_handle.write(content)

def collect_handler_names(file_path: str, keep_prefix: bool) -> str:
    file_text_buffer = open(file_path, "r").read()
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_output_buffer = f"# Scanned bound route handlers for {file_name}:\n"

    # Matches all handler names annotated with @<controller>.route
    handler_match_pattern = "@.+?\.route\(.*?\)\ndef (.+?)\(.*?\).*?:"
    found_handler_names = re.findall(handler_match_pattern, file_text_buffer)

    for handler in found_handler_names:
        prefix = file_name+"." if keep_prefix is True else str()
        file_output_buffer += f"{handler.upper()} = '{prefix}{handler}'\n" 

    return file_output_buffer

if __name__ == "__main__":
    path_scanner_entities = [
        dict(
            file_input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "main.py"), 
            file_output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, \
                "constants/main_endpoint_handler_constants.py"),
            keep_file_prefix = False
        ),
        dict(
            file_input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "auth.py"), 
            file_output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, \
                "constants/auth_endpoint_handler_constants.py"),
            keep_file_prefix = True
        )
    ]
    for entity_dict in path_scanner_entities:
        file, output_source_file, keep_prefix = entity_dict.values()
        file_layout_text = collect_handler_names(file, keep_prefix)
        write_to_file(file_layout_text, output_source_file)