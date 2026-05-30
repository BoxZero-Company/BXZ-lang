# setup.py - Python package installer
from setuptools import setup
import sys
import platform

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bxz-lang",
    version="1.0.0",
    author="BXZ Language Team",
    description="BXZ - A Cross-Platform Polyglot Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["bxz"],
    entry_points={
        "console_scripts": [
            "bxz=bxz:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords="programming language interpreter polyglot",
)