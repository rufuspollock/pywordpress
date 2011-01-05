from setuptools import setup, find_packages
import sys, os

__version__ = '0.1'
try:
    fo = open('README.rst')
    __description__ = fo.read()
    fo.close()
except:
    __description__ = 'A pythonic interface to Wordpress using the Wordpress XML-RPC API'

setup(
    name='pywordpress',
    version=__version__,
    license='mit',
    description=__description__.split('\n')[0],
    long_description=__description__,
    author='Rufus Pollock',
    url='http://bitbucket.org/rgrp/pywordpress/',
    keywords='wordpress python',
    py_modules=['pywordpress'],
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

