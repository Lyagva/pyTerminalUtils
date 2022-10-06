#  Copyright (c) 2022 Lyagva
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup

with open('README.md', "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name='pyterminalutils',
    version='1.0.0',
    author='Lyagva',
    packages=['pyterminalutils'],
    license='GNU GPLv3',
    description='Library with utilities for the terminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "Pillow~=9.2.0",
    ]
)
