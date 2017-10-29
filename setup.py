from setuptools import setup, find_packages
import io
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


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
    name='nbd',

    # Using https://packaging.python.org/en/latest/single_source_version.html
    version=find_version("nbd", "__init__.py"),

    description='Lightweight ipython/jupyter notebook diffing tool',
    long_description=read('README.rst'),

    # project homepage
    url='https://github.com/lcary/nbd',
    download_url='https://github.com/lcary/nbd/archive/v{}.tar.gz'.format(
        find_version("nbd", "__init__.py")),

    author='Luc Cary',
    author_email='luc.cary@gmail.com',
    license='MIT',

    # TODO: support python3
    # Reference: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # maturity
        'Development Status :: 3 - Alpha',

        # who the project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # license (needs to match "license" above)
        'License :: OSI Approved :: MIT License',

        # supported python versions
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    # what the project relates to
    keywords='ipynb jupyter ipython nbconvert git diff git-diff difftool',

    # use find_packages() to find the package
    packages=find_packages(exclude=['demo']),

    # runtime dependencies
    install_requires=['nbconvert', 'nbformat', 'ipython'],

    # entry point to provide executable scripts
    entry_points={
        'console_scripts': [
            'nbd=nbd.main:main',
        ],
    },


)
