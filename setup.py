from distutils.core import setup

from setuptools import find_packages

setup(
    name='acvtool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'javaobj-py3',
        'chameleon',
        'pyyaml==3.12',
        'lxml',
        'six==1.11.0'],
    entry_points={
        'console_scripts': [
            'acv=acvtool:main',
        ]
    }
)
