from setuptools import setup, find_packages
# consistent encoding open():
from codecs import open
import io
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

def read_long_description():
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='ipynb_diff',

    # Using https://packaging.python.org/en/latest/single_source_version.html
    version=find_version("ipynb_diff", "__init__.py"),

    description='ipython notebook diffing tool',
    long_description=read_long_description(),

    # project homepage
    url='https://github.com/lcary/ipynb_diff',

    author='Luc Cary',
    author_email='luc.cary@gmail.com',
    license='MIT',

    # Reference: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # maturity
        'Development Status :: 3 - Alpha',

        # who the project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # license (needs to match "license" above)
        'License :: OSI Approved :: MIT License',

        # supported oython versions
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # what the project relates to
    keywords='ipynb jupyter ipython diff git',

    # use find_packages() to find the package
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'example']),

    # runtime dependencies
    install_requires=['jupyter'],

    # entry point to provide executable scripts
    entry_points={
        'console_scripts': [
            'ipynb_diff=ipynb_diff.main:main',
        ],
    },
)