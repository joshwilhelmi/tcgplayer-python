#!/usr/bin/env python3
"""
Setup script for tcgplayer_client package.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="tcgplayer_client",
    version="1.0.0",
    author="Josh Wilhelmi",
    author_email="josh@gobby.ai",
    description="Python client library for TCGPlayer API with async support, rate limiting, and comprehensive endpoint coverage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshwilhelmi/tcgplayer-python",
    packages=find_packages(where=".", include=["tcgplayer_client*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Clients",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
