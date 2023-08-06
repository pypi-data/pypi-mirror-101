# Copyright 2021 Minseok Yang
# Copyright 2019 New Relic, Inc.
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

from setuptools import setup
from os import path

# Best practice: package name should be prefixed with `newrelic_extension_`
INSTRUMENTED_PACKAGE = "aredis"
PACKAGE_NAME = "newrelic_extension_{}".format(INSTRUMENTED_PACKAGE)
HOOKS = [
    # package_to_intercept = instrumentation_hook
    "aredis = {}.datastore_aredis:instrument".format(PACKAGE_NAME)
]

root_dir = path.abspath(path.dirname(__file__))
with open(path.join(root_dir, "README.rst")) as f:
    DESCRIPTION = f.read()

setup(
    name=PACKAGE_NAME,
    long_description=DESCRIPTION,
    long_description_content_type='text/x-rst',
    version="0.2",
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: "src"},
    entry_points={"newrelic.hooks": HOOKS},
    license="Apache-2.0",
    classifiers=["License :: OSI Approved :: Apache Software License"],
    install_requires=[
        "newrelic",
        # Always require the package being instrumented
        INSTRUMENTED_PACKAGE,
    ],
)
