"""
This module contains the package related functions.
"""
import os
import logging

from file import touch_file


def touch_package(project_name: str, package_name: str, variables: dict[str, str], logger: logging.Logger):
    """
    Create an empty __init__.py file in the package directory
    """
    logger.info(f"Touching package {package_name} ...")
    init_file = os.path.join(package_name, "__init__.py")
    touch_file(project_name, init_file, variables, logger)


def touch_packages(project_name: str, package_names: list[str], variables: dict[str, str], logger: logging.Logger):
    """
    Create an empty __init__.py file in the package directory
    """
    for package_name in package_names:
        touch_package(project_name, package_name, variables, logger)
