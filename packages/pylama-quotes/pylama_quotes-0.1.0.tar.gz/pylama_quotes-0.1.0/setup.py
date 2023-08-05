#!/usr/bin/env python3

"""Main setup script for pylama_quote."""

from glob import glob
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))


def _files(subdir):
    return sorted(set(
        path.join(subdir, path.split(fp)[-1])
        for fp in glob(path.join(here, subdir, '*'))
        if path.isfile(fp)
    ))


if __name__ == '__main__':
    setup(
        name='pylama_quotes',
        version='0.1.0',
        description='Simple quote checker for pylama',
        url='',  # TODO
        author='Craig Kelly',
        author_email='craig.n.kelly@gmail.com',
        license='MIT',

        keywords='pylama quotes static analysis'.split(),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Utilities'
        ],

        packages=[
            'pylama_quotes'
        ],

        entry_points={
            'pylama.linter': ['quotes = pylama_quotes.linter_quotes:Linter']
        },

        scripts=[],
        install_requires=[],
        setup_requires=['pylama>=7.3.3'],
        tests_require=['pylama>=7.3.3'],
        package_data={},
        data_files=[],
    )
