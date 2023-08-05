# AWS Data API SDK for Python
#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from io import open
from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-data-api-python-sdk',
    package_dir={'': 'src'},
    version='0.9.0b1',
    description='Python module to access AWS Data API\'s.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ian Meyers',
    author_email='meyersi@amazon.com',
    license="Apache-2.0",
    url='http://github.com/awslabs/aws-data-api-python-sdk',
    keywords=['aws', 'lambda', 'chalice', 'data-api'],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities']
)
