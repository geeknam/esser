
from setuptools import setup

setup(
    name='esser',
    packages=['esser'],
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
    install_requires=['pynamodb', 'cerberus']
)
