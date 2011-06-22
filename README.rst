A pythonic interface to Wordpress using the Wordpress XML-RPC API.

Source code: https://bitbucket.org/rgrp/pywordpress

Damaged goods: https://bitbucket.org/meatballhat/pywordpress


Usage
=====

Python library
--------------

Read the code documentation::

    >>> from pywordpress import Wordpress
    >>> help(Wordpress)


Development
===========

To run the rests you will need to:

1. Create a wordpress install for the tests to interact with (WARNING: the
   tests delete pages on teardown. DO NOT test this code against a
   wordpress instance containing data you care about).

2. Create a config file called test.ini in the directory you will run the tests
   from::

    cp config.ini.tmpl test.ini
    # edit test.ini to reflect location and login or your test instance
    vi test.ini
    ...

To run the tests then do::

    python test_pywordpress.py


Author
======

Rufus Pollock - http://rufuspollock.org/


Jerkface
========

Dan Buch - http://meatballhat.com/


License
=======

MIT-licensed: http://www.opensource.org/licenses/mit-license.php

