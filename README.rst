A pythonic interface to Wordpress using the Wordpress XML-RPC API.

Source code: https://github.com/rgrp/pywordpress


Usage
=====

Command line
------------

Check out the commands::

    wordpress.py -h 

You will need to create a config with the details (url, login) of the wordpress
instance you want to work with::

    cp config.ini.tmpl config.ini
    # now edit away ...
    vim config.ini


Python library
--------------

Read the code documentation::

    >>> from pywordpress import Wordpress
    >>> help(Wordpress)


Development
===========

To run the tests you will need to:

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

