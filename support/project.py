"""
This module contains the Project class and ProjectCreator class.
"""

import os
import logging

from support.package import touch_packages
from support.file import touch_file, touch_files
from support.dependency import get_dependency_version, add_dependency


class Project:
    """
    This class represents a project
    """
    name: str
    path: str

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = os.path.join(path, name)

    def __str__(self):
        return f"Project({self.name})"

    def __repr__(self):
        return f"Project({self.name})"

    def exists(self) -> bool:
        """
        Check if the project exists

        :return: True if the project exists, False otherwise
        """
        if not os.path.exists(self.path):
            return False

        return True


class ProjectCreator:
    """
    This class is responsible for creating a new project.
    """
    projects_dir: str
    logger: logging.Logger

    def __init__(self, projects_dir: str, logger: logging.Logger):
        """
        Initialize the ProjectCreator class

        :param projects_dir: The directory where the projects are stored
        """
        self.projects_dir = projects_dir
        self.logger = logger

    def create(self, name: str, variables=None) -> Project:
        """
        Create a new project instance

        :param name: The name of the project
        :param variables: The variables to use when creating the project
        :return: A new Project instance
        """
        if variables is None:
            variables = {}

        self.logger.info(f"Creating project: {name}")

        project = Project(name, self.projects_dir)

        if not project.exists():
            self.logger.info(f"Creating project directory: {project.path}")
            os.makedirs(project.path, exist_ok=True)

        package_names = [".", name, "tests"]
        file_names = ["README.md", "requirements.txt", "setup.py", "setup.cfg", "Makefile", "VERSION"]

        touch_packages(project.name, package_names, variables, self.logger)
        touch_files(project.name, file_names, variables, self.logger)
        touch_file(project.name, "docs/index.md", variables, self.logger)

        add_dependency(project.name, "pytest", self.logger)
        add_dependency(project.name, "flake8", self.logger)
        add_dependency(project.name, "black", self.logger)
        add_dependency(project.name, "pylint", self.logger)
        add_dependency(project.name, "python-dotenv", self.logger)

        return project
