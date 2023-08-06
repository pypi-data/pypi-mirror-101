# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
# Modifications Copyright 2021 MatheusCod, juliokiyoshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="powerboard",
    version="0.0.1",
	author="MatheusCod, juliokiyoshi",
    author_email="openpower@ic.unicamp.br",
    description="Energy Profiling plugin for TensorBoard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Unicamp-OpenPower/PowerBoard",
    project_urls={
        "Bug Tracker": "https://github.com/Unicamp-OpenPower/PowerBoard/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=["powerboard"],
    package_data={
        "powerboard": ["static/**"],
    },
    entry_points={
        "tensorboard_plugins": [
            "powerboard = powerboard.plugin:PowerBoard",
        ],
    },
)
