
from setuptools import setup, find_packages

import remediator

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='remediator',
    description='remediates ACP violations',
    author='Leonardo Bautista',
    author_email='leonardo.bautista@accenture.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'remediator=remediator.__main__:handler'
        ]
    }
)
