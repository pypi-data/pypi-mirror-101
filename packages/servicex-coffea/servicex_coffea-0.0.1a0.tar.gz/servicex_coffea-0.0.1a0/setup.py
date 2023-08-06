import os
from setuptools import setup

version = os.getenv('servicex_version')
if version is None:
    version = '0.1a1'
else:
    version = version.split('/')[-1]

setup(version=version)
