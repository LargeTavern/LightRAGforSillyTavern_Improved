from setuptools import setup, find_packages
from pathlib import Path

def read_long_description():
    try:
        return Path("README.md").read_text(encoding="utf-8")
    except FileNotFoundError:
        return "A LightRAG implementation for SillyTavern"

def read_requirements():
    try:
        with open("requirements.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Warning: 'requirements.txt' not found.")
        return []

setup(
    name="lightragst",
    version="0.1.0",
    description="LightRAG implementation for SillyTavern",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests*",)),
    python_requires=">=3.9",
    install_requires=read_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)