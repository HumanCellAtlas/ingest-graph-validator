#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from os import path
from setuptools import setup, find_packages

requirements = [
    "argcomplete==1.10.3",
    "atomicwrites==1.3.0",
    "boto3==1.10.28",
    "botocore==1.13.28",
    "cachetools==3.1.1",
    "certifi==2019.11.28",
    "cffi==1.13.2",
    "chardet==3.0.4",
    "Click==7.0",
    "colorama==0.4.1",
    "commonmark==0.9.1",
    "coverage==4.5.4",
    "crc32c==1.7",
    "cryptography==2.8",
    "dcplib==2.1.2",
    "docker==4.1.0",
    "docutils==0.15.2",
    "et-xmlfile==1.0.1",
    "google-auth==1.7.1",
    "google-auth-oauthlib==0.4.1",
    "hca==6.5.1",
    "hca-ingest==0.6.8",
    "idna==2.8",
    "jdcal==1.4.1",
    "Jinja2==2.10.3",
    "jmespath==0.9.4",
    "jsonpointer==1.14",
    "jsonref==0.2",
    "jsonschema==2.6.0",
    "MarkupSafe==1.1.1",
    "neobolt==1.7.15",
    "neotime==1.7.4",
    "oauthlib==3.1.0",
    "openpyxl==3.0.2",
    "polling==0.3.1",
    "prompt-toolkit==2.0.10",
    "puremagic==1.4",
    "py2neo==4.3.0",
    "pyasn1==0.4.8",
    "pyasn1-modules==0.2.7",
    "pycparser==2.19",
    "Pygments==2.3.1",
    "PyJWT==1.7.1",
    "pyOpenSSL==19.1.0",
    "python-dateutil==2.8.0",
    "pytz==2019.3",
    "PyYAML==5.1.2",
    "requests==2.22.0",
    "requests-oauthlib==1.3.0",
    "rsa==4.0",
    "s3transfer==0.2.1",
    "six==1.13.0",
    "tenacity==5.0.4",
    "tqdm==4.39.0",
    "tweak==1.0.3",
    "urllib3==1.24.3",
    "wcwidth==0.1.7",
    "websocket-client==0.56.0",
    "XlsxWriter==1.2.6",
]

setup_requirements = ["pytest-runner", ]

test_requirements = ["pytest>=3", ]

# Description from readme.
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    author="Javier Ferrer Gómez",
    author_email="jferrer@ebi.ac.uk",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="HCA Ingest Service neo4j graph validator package",
    entry_points={
        'console_scripts': [
            "ingest-graph-validator=ingest_graph_validator.ingest_graph_validator:entry_point",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="ingest-graph-validator",
    name="ingest-graph-validator",
    packages=find_packages(include=["ingest_graph_validator", "ingest_graph_validator.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/HumanCellAtlas/ingest-graph-validator",
    version="0.4.0",
    zip_safe=False,
)
