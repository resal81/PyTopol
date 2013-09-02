#!/usr/bin/env python

import os
import sys
from setuptools.command.test import test as TestCommand
import pytopol

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the
        #eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


#readme = open('README.md').read()
doclink = """
Documentation
=============

Plese see http://github.com/resal81/pytopol"""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pytopol',
    version=pytopol.__version__,
    description='"Library for converting molecular topologies"',
    long_description= doclink + '\n\n' + history,
    author='Reza Salari',
    author_email='rezasalari@rutgers.edu',
    url='https://github.com/resal81/pytopol',
    packages=[
        'pytopol',
    ],
    package_dir={'pytopol': 'pytopol'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='pytopol',
    scripts=['scripts/psf2top.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    tests_require=['pytest>=2.3.5'],
    cmdclass={'test': PyTest},
)
