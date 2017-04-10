
from setuptools import setup

packages = [
    'esser',
    'esser.cli',
    'esser.contrib',
    'esser.handlers',
    'esser.infra',
    'esser.repositories'
]

setup(
    name='esser',
    packages=packages,
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
