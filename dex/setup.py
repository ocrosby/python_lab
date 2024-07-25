import os

from setuptools import setup, find_packages


def read(name):
    """Utility function to read a file"""
    return open(os.path.join(os.path.dirname(__file__), name)).read()

# https://pythonhosted.org/an_example_pypi_project/setuptools.html


setup(
    name='dex',
    version=read('VERSION').strip(),
    # scripts=['./scripts/myscript'],
    author="Omar Crosby",
    author_email="omar.crosby@gmail.com",
    description="A simple HTTP client for making batched requests.",
    keywords="http client batch requests",
    packages=["dex", "tools"],
    long_description=read('README.md'),
    install_requires=[
        # List your project's dependencies here.
        # e.g., 'requests>=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'dex=dex.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.9',
)
