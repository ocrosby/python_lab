#!/usr/bin/env python3

import sys
import logging

import yaml

from support.project import ProjectCreator


def read_variables_from_file(file_path: str) -> dict:
    """
    Read variables from a file

    :param file_path: The path to the file
    :return: The variables
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    """
    Main function
    """
    # Create a logger
    return_code = 0

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("create_project")

    logger.info("Startup")

    if len(sys.argv) != 2:
        print("Usage: python create.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]

    try:
        variables = read_variables_from_file("variables.yaml")
        creator = ProjectCreator("projects", logger)
        project = creator.create(project_name, variables)

        logger.info(f"Project created: {project}")
        logger.info(f"Project path: {project.path}")
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return_code = 1
    finally:
        logger.info("Done")

    logger.info("Shutdown")
    sys.exit(return_code)


if __name__ == "__main__":
    main()
