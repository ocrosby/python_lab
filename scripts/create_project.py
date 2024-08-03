import os
import sys


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


def touch_file(project_name: str, file_name: str):
    """
    Create an empty file in the project directory
    """
    if not file_exists(project_name, file_name):
        write_file(project_name, file_name, "")

def touch_package(project_name: str, package_name: str):
    """
    Create an empty __init__.py file in the package directory
    """
    touch_file(project_name, os.path.join(package_name, "__init__.py")


def create_project(project_name: str):
    # Create project directory
    touch_file(project_name, "__init__.py")
    touch_file(project_name, "README.md")
    touch_file(project_name, "requirements.txt")
    touch_file(project_name, "setup.py")
    touch_file(project_name, "setup.cfg")
    touch_file(project_name, "src/main.py")


def main():
    if len(sys.argv) != 2:
        print("Usage: python create_project.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    print(f"Creating project: {project_name}")
    create_project(project_name)


if __name__ == "__main__":
    main()
