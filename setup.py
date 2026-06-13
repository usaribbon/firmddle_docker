from pathlib import Path

from setuptools import find_packages, setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")


setup(
    name="firmddle",
    version="0.1.0a0",
    description="Firmware evidence extraction and backdoor clue hunting CLI.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/usaribbon/firmddle_docker",
    license="Apache-2.0",
    packages=find_packages(include=["firmddle", "firmddle.*"]),
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Security",
    ],
    entry_points={"console_scripts": ["firmddle=firmddle.cli:main"]},
)
