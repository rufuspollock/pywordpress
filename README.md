A pythonic interface to Wordpress using the Wordpress XML-RPC API.

Source code: https://github.com/rufuspollock/pywordpress


## Usage

### Command line

Check out the commands:

    pywordpress.py -h 

Commands and methods:

* `create_many_pages`: Create many pages at once (and only create pages which do not already exist).
* `delete_all_pages`: Delete all pages (i.e. delete_page for each page in instance).
* `delete_page`: http://codex.wordpress.org/XML-RPC_wp#wp.deletePage
* `edit_page`: http://codex.wordpress.org/XML-RPC_wp#wp.editPage
* `get_authors`: http://codex.wordpress.org/XML-RPC_wp#wp.getAuthors
* `get_categories`: http://codex.wordpress.org/XML-RPC_wp#wp.getCategories
* `get_page`: http://codex.wordpress.org/XML-RPC_wp#wp.getPage
* `get_page_list`: http://codex.wordpress.org/XML-RPC_wp#wp.getPageList
* `get_pages`: http://codex.wordpress.org/XML-RPC_wp#wp.getPages
* `get_tags`: http://codex.wordpress.org/XML-RPC_wp#wp.getTags
* `get_comments`: https://codex.wordpress.org/XML-RPC_WordPress_API/Comments#wp.getComments
* `init_from_config`: Class method to initialize a `Wordpress` instance from an ini file.
* `new_page`: http://codex.wordpress.org/XML-RPC_wp#wp.newPage

You can use these both from the command line and the library:

```
# command line
pywordpress.py get_comments

# in python
wp = pywordpress.Wordpress.init_from_config('config.ini')
pages= wp.get_pages()
print(pages)
```

You will need to create a config with the details (url, login) of the wordpress
instance you want to work with:

    cp config.ini.tmpl config.ini
    # edit the config with your details
    vim config.ini


### Python Library

Read the code documentation::

    >>> from pywordpress import Wordpress
    >>> help(Wordpress)

Here's an example that downloads all of a sites pages to a CSV file:

```python=
import pywordpress

# pip install backports.csv
# use python 3 csv library that supports unicode as Wordpress pages are utf8 encoded
from backports import csv
import io

# use site details and login from config
wp = pywordpress.Wordpress.init_from_config('config.ini')

def write_to_csv(filename, list_of_pages_or_posts):
    fo = io.open(filename, 'w', newline='', encoding='utf-8')
    fieldnames = list_of_pages_or_posts[0].keys()
    writer = csv.DictWriter(fo, fieldnames)
    writer.writeheader()
    writer.writerows(list_of_pages_or_posts)

# get the first 100 pages
out = wp.get_pages(100)
print('Number of pages: %s' % len(out))

# write the list of pages to the CSV files
write_to_csv('pages.csv', out)
```

Here's a more elaborate version that saves all posts and pages ...

```
import pywordpress

# pip install backports.csv
# use python 3 csv library that supports unicode as Wordpress pages are utf8 encoded
from backports import csv
import io

# use site details and login from config
wp = pywordpress.Wordpress.init_from_config('config.ini')

def write_to_csv(filename, list_of_pages_or_posts):
    fo = io.open(filename, 'w', newline='', encoding='utf-8')
    fieldnames = list_of_pages_or_posts[0].keys()
    writer = csv.DictWriter(fo, fieldnames)
    writer.writeheader()
    writer.writerows(list_of_pages_or_posts)

def do_pages():
    out = wp.get_pages(100)
    print('Number of pages: %s' % len(out))
    write_to_csv('pages.csv', out)

def do_posts():
    # total posts (you can check this yourself in your wordpress admin section)
    total = 588
    chunk_size = 100
    chunks = 1 + (total / chunk_size)
    out = []
    count = 0
    while count < chunks:
        items = wp.get_posts(filter={'number': chunk_size, 'offset':
            chunk_size*count})
        out.extend(items)
        count += 1
    print('Number of posts: %s' % len(out))
    write_to_csv('posts.csv', out)

do_pages()
do_posts()
```

## Development

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


## Author

Rufus Pollock - http://rufuspollock.org/

## License

MIT-licensed: http://www.opensource.org/licenses/mit-license.php

