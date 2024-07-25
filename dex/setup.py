from setuptools import setup, find_packages

setup(
    name='src',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
        # e.g., 'requests>=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'src=src.main:main',
        ],
    },
)
