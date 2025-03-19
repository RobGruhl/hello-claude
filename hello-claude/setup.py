from setuptools import setup, find_packages

setup(
    name="hello_claude",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "qtpy>=2.3.0",
        "PySide6>=6.4.0",
    ],
    entry_points={
        "console_scripts": [
            "hello-claude=hello_claude.main:main",
        ],
    },
)