from setuptools import setup, find_packages

setup(
    name='dex',
    version='0.1.0',
    packages=find_packages(include=['utils']),
    install_requires=[
        # List your project's dependencies here.
        # e.g., 'requests>=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'dex=dex.main:main',
        ],
    },
)
