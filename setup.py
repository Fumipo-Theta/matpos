# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='matpos',
    version='1.0.0',
    description='Ease custum layout of subplots for matplotlib',
    long_description=readme,
    author='Fumitoshi Morisato',
    author_email='fmorisato@gmail.com',
    url='https://github.com/Fumipo-Theta/matpos',
    install_requires=['numpy', 'matplotlib', 'func_helper'],
    dependency_links=[
        'git+ssh://git@github.com/Fumipo-Theta/func_helper#egg=func_helper@master#egg=func_helper-1.0.0'],
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
