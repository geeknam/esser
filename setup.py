from setuptools import find_packages
from setuptools import setup

setup(
    name='esser',
    packages=find_packages(
        exclude=[
            'examples.*', 'examples', 'tests', 'requirements',
            'docs'
        ]
    ),
    license='Apache 2.0',
    version='0.1.1',
    description='Python Event Sourcing framework',
    long_description=open('README.md').read(),
    author='Nam Ngo',
    author_email='namngology@gmail.com',
    url='https://geeknam.github.io/esser',
    keywords=[
        'event sourcing', 'framework', 'esser', 'serverless',
        'dynamodb', 'lambda'
    ],
    install_requires=['pynamodb', 'cerberus'],
    entry_points={
        'console_scripts': [
            'esser = esser.cli.run:main'
        ]
    },
)
