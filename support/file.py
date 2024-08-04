import os
import logging

from string import Template


def process_template(template_path: str, output_path: str, variables: dict[str, str], logger: logging.Logger):
    """
    Process a template file and write the output to a new file.

    :param template_path: The path to the template file
    :param output_path: The path to the output file
    :param variables: A dictionary of variables to substitute in the template
    """
    logger.info(f"Processing template '{template_path}' ...")

    if variables is None:
        variables = {}

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    template = Template(template_content)

    try:
        processed_content = template.substitute(variables)
    except Exception as e:
        print(f"Error processing template '{template_path}': {e}")
        return

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(processed_content)


def generate_relative_path(project_name: str, file_name: str):
    """
    Generate a relative path to a file in the project directory
    """
    cwd = os.getcwd()
    file_path = os.path.join("projects", project_name, file_name)
    rel_path = os.path.relpath(file_path, cwd)

    return rel_path


def write_file(project_name: str, file_name: str, contents: str = ""):
    """
    Write contents to a file in the project directory
    """

    # Create file
    file_path = generate_relative_path(project_name, file_name)

    # Extract the directory path from the file path
    dir_path = os.path.dirname(file_path)

    # Create all parent directories if they don't already exist
    os.makedirs(dir_path, exist_ok=True)

    # Create the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(contents)


def file_exists(project_name: str, file_name: str):
    rel_path = generate_relative_path(project_name, file_name)
    return os.path.exists(rel_path)


def get_template_path(file_name: str):
    """
    Get the path to a template file
    """
    return os.path.join("templates", f"{file_name}.template")


def has_template(file_name: str):
    """
    Check if a file has a template
    """
    template_path = get_template_path(file_name)
    return os.path.isfile(template_path)


def is_essentially_empty(project_name: str, file_name: str):
    """
    Check if a file in the project directory is essentially empty
    """
    rel_path = generate_relative_path(project_name, file_name)

    if not os.path.exists(rel_path):
        return True

    with open(rel_path, 'r', encoding='utf-8') as file:
        contents = file.read()

    contents = contents.strip()

    return len(contents) == 0


def touch_file(project_name: str, file_name: str, variables, logger: logging.Logger):
    """
    Create a new file in the project directory
    """
    logger.info(f"Touching file {file_name} ...")

    if variables is None:
        variables = {}

    template_path = get_template_path(file_name)
    output_path = generate_relative_path(project_name, file_name)

    if file_exists(project_name, file_name):
        if is_essentially_empty(project_name, file_name) and has_template(file_name):
            process_template(template_path, output_path, variables, logger)
    else:
        if has_template(file_name):
            process_template(template_path, output_path, variables, logger)
        else:
            write_file(project_name, file_name)


def touch_files(project_name: str, file_names: list[str], variables, logger: logging.Logger):
    """
    Create an empty file in the project directory
    """
    if variables is None:
        variables = {}
    for file_name in file_names:
        touch_file(project_name, file_name, variables, logger)
