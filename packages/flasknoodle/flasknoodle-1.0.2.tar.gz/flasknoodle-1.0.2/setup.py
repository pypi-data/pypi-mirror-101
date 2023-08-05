import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "ReadMe.md").read_text()

# This call to setup() does all the work
setup(
    name="flasknoodle",
    version="1.0.2",
    description="flask project generator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/odunet/Flask_ProjectGenerator",
    author="Ayokunle Odutayo",
    author_email="odunet2000@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["doodle"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "flasknoodle=doodle.__main__:main",
        ]
    },
)