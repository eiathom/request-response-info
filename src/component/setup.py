"""request-response-info setup"""

import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='request-response-info',
    version='1.0.0',
    author='eiathom',
    author_email='eiathom@protonmail.ch',
    url='https://github.com/eiathom/request-response-info',
    description='Perform URL requests and display response data',
    license='Apache 2.0',
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Other Audience',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Computer/Technology',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # test requirements
        'pytest',
        'mock'
    ],
    setup_requires=[
        'pytest-runner'
    ]
)
