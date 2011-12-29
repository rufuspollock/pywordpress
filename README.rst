A pythonic interface to Wordpress using the Wordpress XML-RPC API.

Source code: https://github.com/rgrp/pywordpress


Usage
=====

Command line
------------

Check out the commands::

    wordpress.py -h 

Commands::

    create_many_pages: Create many pages at once (and only create pages which do not already exist).
    delete_all_pages: Delete all pages (i.e. delete_page for each page in instance).
    delete_page: http://codex.wordpress.org/XML-RPC_wp#wp.deletePage
    edit_page: http://codex.wordpress.org/XML-RPC_wp#wp.editPage
    get_authors: http://codex.wordpress.org/XML-RPC_wp#wp.getAuthors
    get_categories: http://codex.wordpress.org/XML-RPC_wp#wp.getCategories
    get_page: http://codex.wordpress.org/XML-RPC_wp#wp.getPage
    get_page_list: http://codex.wordpress.org/XML-RPC_wp#wp.getPageList
    get_pages: http://codex.wordpress.org/XML-RPC_wp#wp.getPages
    get_tags: http://codex.wordpress.org/XML-RPC_wp#wp.getTags
    init_from_config: Class method to initialize a `Wordpress` instance from an ini file.
    new_page: http://codex.wordpress.org/XML-RPC_wp#wp.newPage


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

