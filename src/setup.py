#
# Setup file to use with pip:
#        pip3 install --user ./src
#

import os
from typing import Any

from setuptools import find_packages, setup


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_list(file_path):
    if not os.path.isfile(file_path):
        return []
    ret_list = []
    with open(file_path, encoding="utf-8") as content_file:
        for line in content_file:
            if line.startswith("git"):
                ## skip -- setuptools does not support installing packages from git remote repo
                continue
            ret_list.append(line.strip())
    return ret_list


packages_list = find_packages(include=["linakdeskapp", "linakdeskapp.*"])

## additional data to install
packages_data: dict[str, Any] = {"linakdeskapp": []}

## additional scripts to install
additional_scripts: list[str] = []

requirements_path = os.path.join(SCRIPT_DIR, "requirements.txt")
install_reqs = read_list(requirements_path)

## every time setup info changes then version number should be increased

setup(
    name="linakdeskapp",
    version="1.0.1",
    description="desktop application that allows control of Linak office desk under Linux",
    url="https://github.com/anetczuk/LinakDeskApp",
    author="Arkadiusz Netczuk",
    license="MIT",
    packages=packages_list,
    package_data=packages_data,
    scripts=additional_scripts,
    install_requires=install_reqs,
)
