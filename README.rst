A pythonic interface to Wordpress using the Wordpress XML-RPC API.

Source code: https://bitbucket.org/rgrp/pywordpress


Usage
=====

Command line
------------

First you'll need to create a config.ini::

    cp config.ini.tmpl config.ini

Now edit this config.ini to have the config for the wordpress instance you want
to work with.

Now check out the commands::

    wordpress.py -h 

Python library
--------------

Usage::

    pydoc pywordpress.Wordpress
    # or
    >>> from pywordpress import Wordpress
    >>> help(Wordpress)


Development
===========

To run the rests you will need to:

1. Create a wordpress install for the tests to interact with (WARNING: the
   tests delete all pages on teardown. DO NOT test this code against a
   wordpress instance containing data you care about).

2. Create a config file called test.ini in the directory you will run the tests
   from::

    cp config.ini.tmpl test.ini
    # edit test.ini to reflect location and login or your test instance
    vi test.ini
    ...

To run the tests then do::

    nosetests test_pywordpress.py


Author
======

Rufus Pollock - http://rufuspollock.org/

License
=======

MIT-licensed: http://www.opensource.org/licenses/mit-license.php

