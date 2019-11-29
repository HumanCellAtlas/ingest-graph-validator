#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Javier Ferrer",
    author_email='jferrer@ebi.ac.uk',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="HCA Ingest Service neo4j graph validator package",
    entry_points={
        'console_scripts': [
            'ingest_graph_validator=ingest_graph_validator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description='placeholder',
    include_package_data=True,
    keywords='ingest_graph_validator',
    name='ingest_graph_validator',
    packages=find_packages(include=['ingest_graph_validator', 'ingest_graph_validator.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/javfg/ingest_graph_validator',
    version='0.1.0',
    zip_safe=False,
)
