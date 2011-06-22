try:
    from packaging import setup
except ImportError:
    try:
        from distutils2 import setup
    except ImportError:
        from setuptools import setup


__version__ = '0.1'
try:
    fo = open('README.rst')
    __description__ = fo.read()
    fo.close()
except (IOError, OSError):
    __description__ = \
        'A pythonic interface to Wordpress using the Wordpress XML-RPC API'

setup(
    name='pywordpress',
    version=__version__,
    license='MIT',
    description=__description__.split('\n')[0],
    long_description=__description__,
    author='Rufus Pollock',
    url='http://bitbucket.org/rgrp/pywordpress/',
    keywords='wordpress python',
    py_modules=['pywordpress'],
    zip_safe=False,
    test_suite='nose.collector',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

