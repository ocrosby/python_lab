import os
import logging
import http.client
import json

from typing import Optional


def get_dependency_version(dependency_name: str, logger: logging.Logger) -> Optional[str]:
    """
    Search PyPi for the current version of a dependency if not found return None otherwise report the version.

    :param dependency_name: The name of the dependency
    :return: The version of the dependency
    """
    version = None
    conn = http.client.HTTPSConnection("pypi.org")

    try:
        conn.request("GET", f"/pypi/{dependency_name}/json")
        res = conn.getresponse()

        if res.status != 200:
            return None

        data = json.loads(res.read().decode())
        version = data.get("info", {}).get("version")
    except Exception as e:
        logger.error(f"Error getting dependency version: {e}")
    finally:
        conn.close()

    return version


def has_dependency(project_name: str, dependency_name: str):
    """
    Check if a dependency is already added to the project

    :param project_name: The name of the project
    :param dependency_name: The name of the dependency
    :return: True if the dependency is already added, False otherwise
    """
    # Generate the path to the requirements file
    requirements_file = os.path.join("projects", project_name, "requirements.txt")

    if not os.path.isfile(requirements_file):
        return False

    # Check if the dependency is already added to the requirements file
    with open(requirements_file, "r") as f:
        return dependency_name in f.read()


def add_dependency(project_name: str, dependency_name: str, logger: logging.Logger):
    """
    Add a dependency to the project

    :param project_name: The name of the project
    :param dependency_name: The name of the dependency
    """

    # Check if the dependency is already added
    if has_dependency(project_name, dependency_name):
        logger.info(f"Dependency {dependency_name} is already added to the project")
        return

    logger.info(f"Adding dependency {dependency_name} to the project {project_name} ...")

    # Generate the path to the requirements file
    requirements_file = os.path.join("projects", project_name, "requirements.txt")

    # Determine the version of the dependency
    version = get_dependency_version(dependency_name, logger)

    # Add the dependency to the requirements file
    with open(requirements_file, "a", encoding="utf-8") as f:
        if version is None:
            logger.info(f"The version of the dependency {dependency_name} could not be determined")
            f.write(f"{dependency_name}\n")
        else:
            logger.info(f"The version of the dependency {dependency_name} is {version}")
            f.write(f"{dependency_name}=={version}\n")


