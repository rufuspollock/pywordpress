#!/usr/bin/env python
from __future__ import with_statement, print_function

import inspect
import optparse
import pprint
import sys
import itertools
import re

try:
    from xmlrpc.client import ServerProxy
    from configparser import ConfigParser
except ImportError:
    from xmlrpclib import ServerProxy
    from ConfigParser import SafeConfigParser as _ConfigParser

    class ConfigParser(_ConfigParser):
        read_file = _ConfigParser.readfp

class Cache(object):
    ''' The page cache for wordpress

    Sample usage::

    >>> import pywordpress
    >>> wp = pywordpress.Wordpress('http://wp.site.com/', 'my-username', 'my-password')
    >>> c=pywordpress.Cache(cachefile=".cache", wordpress=wp)
    >>> c.get_page(0)
    >>> 
    '''

    def __init__(self, cachefile=None, wordpress=None):
        import pickle,atexit
        self.cachefile=cachefile
        self.wp=wordpress
        if cachefile:
            try:
                f=open(cachefile,"rb")
                self.pages=pickle.load(f)
                f.close()
            except IOError:
                self.pages={}
            except EOFError:
                self.pages={}
            atexit.register(self.write)
        else:  
            self.pages={}
  
    def write(self):
        ''' write the cache file - this is called automatically on exit '''
        import pickle
        try:
            f=open(self.cachefile,"wb")
            pickle.dump(self.pages,f)
            f.close()
        except IOError:
            print("Can't write cache file")

    def get_and_cache_page(self,page_id):
        page=self.wp._get_page(page_id)
        self.pages[str(page_id)]=page
        return page
    
    def get_page(self, page_id):
        ''' get the page with page_id from the cache
          if the page does not exist in the cache, get it from wordpress and
          cache the result '''
        page=self.pages.get(str(page_id))
        if not page:
            page=self.get_and_cache_page(page_id)
        return page

    def get_changed_pages(self,page_dict,existing_pages):
        def ischanged(page):  
              slug=re.sub("^/|/$","",page[0])
              content=page[1]
              if slug in existing_pages:
                return content['description']!=existing_pages[slug]['description']
              else:
                return True
        return dict(itertools.ifilter(ischanged, page_dict.items()))
    
class Wordpress(object):
    '''Interact with an existing wordpress install via xml-rpc

    Sample usage::

        >>> from pywordpress import Wordpress
        >>> wp = Wordpress('http://wp.site.com/', 'my-username', 'my-password')
        >>> page_list = wp.get_page_list()
        ...
        >>> new_page_id = w.new_page(title='Title', description='Our content')
        >>> new_page = wp.get_page(new_page_id)
        >>> print(new_page['title'])
        Title
        >>> 
    '''

    def __init__(self, wp_url, username, password, blog_id=0, verbose=False, delay=None, cache=False, cachefile=None):
        self.user = username
        self.password = password
        self.wp_url = wp_url
        xmlrpc_url = wp_url.rstrip('/') + '/xmlrpc.php'
        self.server = ServerProxy(xmlrpc_url)
        self.blog_id = blog_id
        self.verbose = verbose
        self.delay=delay
        if cache:
            self.cache=Cache(cachefile=cachefile,wordpress=self)
        else:
            self.cache=None

    @classmethod
    def init_from_config(self, config_fp):
        '''Class method to initialize a `Wordpress` instance from an ini file.

        For an example ini file see config.ini.tmpl
        '''
        cfg = ConfigParser()
        with open(config_fp) as infile:
            cfg.read_file(infile)

        wp_url = cfg.get('wordpress', 'url')
        wp_user = cfg.get('wordpress', 'user')
        wp_password = cfg.get('wordpress', 'password')
        wp_cachefile = cfg.get('wordpress', 'cachefile',None)
        if wp_cachefile:
            wp_cache=True
        else:
            wp_cache=False  
        return self(wp_url, wp_user, wp_password, verbose=True, delay=int(cfg.get("wordpress","delay",0)), cache=wp_cache, cachefile=wp_cachefile)

    def _print(self, msg):
        if self.verbose:
            print(msg)

    def get_page_list(self):
        '''http://codex.wordpress.org/XML-RPC_wp#wp.getPageList'''
        results = self.server.wp.getPageList(
            self.blog_id,
            self.user,
            self.password
        )
        return results

    def get_page(self, page_id):
        if self.cache:
            return self.cache.get_page(page_id)
        else: 
            return self._get_page(page_id)
        
    def _get_page(self, page_id):
        '''http://codex.wordpress.org/XML-RPC_wp#wp.getPage'''
        results = self.server.wp.getPage(
            self.blog_id,
            page_id,
            self.user,
            self.password
        )
        if self.delay:
            import time
            time.sleep(self.delay)
        return results

    def get_pages(self, max_pages=10):
        '''http://codex.wordpress.org/XML-RPC_wp#wp.getPages'''
        results = self.server.wp.getPages(
            self.blog_id,
            self.user,
            self.password,
            max_pages
        )
        return results

    def get_posts(self,filter=None):
        '''http://codex.wordpress.org/XML-RPC_WordPress_API/Posts#wp.getPosts'''
        if filter:
            results = self.server.wp.getPosts(
                self.blog_id,
                self.user,
                self.password,
                filter
                )
        else:
            results = self.server.wp.getPosts(
                self.blog_id,
                self.user,
                self.password
                )
        return results

    def get_post(self, post_id):
        '''http://codex.wordpress.org/XML-RPC_WordPress_API/Posts#wp.getPost'''
        results = self.server.wp.getPost(
            self.blog_id,
            self.user,
            self.password,
            post_id)
        if self.delay:
            import time
            time.sleep(self.delay)
        return results

    def get_authors(self):
        """http://codex.wordpress.org/XML-RPC_wp#wp.getAuthors"""
        results = self.server.wp.getAuthors(
            self.blog_id,
            self.user,
            self.password
        )
        return results

    def get_categories(self):
        """http://codex.wordpress.org/XML-RPC_wp#wp.getCategories"""
        results = self.server.wp.getCategories(
            self.blog_id,
            self.user,
            self.password
        )
        return results

    def get_tags(self):
        """http://codex.wordpress.org/XML-RPC_wp#wp.getTags"""
        results = self.server.wp.getTags(
            self.blog_id,
            self.user,
            self.password
        )
        return results

    def new_page(self, **kwargs):
        '''http://codex.wordpress.org/XML-RPC_WordPress_API/Pages#wp.newPage

        All options are supported, e.g. to set comments on pass

            mt_allow_comments='open'
        
        :param **kwargs: all other possible arguments for content struct (see
        WP docs).
        '''
        content_struct = dict(kwargs)
        if not 'mt_allow_comments' in content_struct:
            content_struct['mt_allow_comments'] = 0
        if not 'mt_allow_pings' in content_struct:
            content_struct['mt_allow_pings'] = 0
        publish = True

        page_id = self.server.wp.newPage(
            self.blog_id,
            self.user,
            self.password,
            content_struct,
            publish
        )
        page_id = int(page_id)
        return page_id
        
    def delete_page(self, page_id):
        '''http://codex.wordpress.org/XML-RPC_wp#wp.deletePage'''
        result = self.server.wp.deletePage(
            self.blog_id,
            self.user,
            self.password,
            page_id
        )
        return bool(result)

    def delete_all_pages(self):
        '''Delete all pages (i.e. delete_page for each page in instance).
        '''
        for pagedict in self.get_page_list():
            self._print('Deleting: %s' % pagedict)
            self.delete_page(pagedict['page_id'])

    def edit_page(self, page_id, **kwargs):
        '''http://codex.wordpress.org/XML-RPC_wp#wp.editPage

        Note: editing a page leads to a new revision.

        :param **kwargs: attribute values for content struct (see wordpress docs).
        '''
        # existing values not in content_struct are *not* left alone but are
        # set to empty string!
        edit_struct = self.get_page(page_id)
        edit_struct.update(kwargs)
        result = self.server.wp.editPage(
            self.blog_id,
            page_id,
            self.user,
            self.password,
            edit_struct
        )

        # if page is cached - update the cache

        if self.cache:
          self.cache.get_and_cache_page(page_id)

        return bool(result)

    def create_many_pages(self, pages_dict):
        '''Create many pages at once (pages which already exist will be edited
        rather than created).

        pages_dict = {
            '/about/': {
                'title': 'ABC',
                'description': 'xxx'
            },
            '/about/people/': {
                'title': 'ABC',
                'description': 'xxx'
            }
        }
        '''
        ## get a list of existing pages keyed by their urls

        ## use get_page_list as that shows trash items as well as active
        pagelist = itertools.ifilter(lambda x: x.get('page_status',None) != 'trash',
        ( self.get_page(x['page_id']) for x in self.get_page_list()))

        pagedict = dict(( (p['page_id'], p) for p in pagelist ))
        def get_page_url(page):
            parent_id = page['wp_page_parent_id']
            if parent_id == 0:
                return page['wp_slug']
            else:
                return get_page_url(pagedict[parent_id]) + '/' + page['wp_slug']
        existing_pages = dict(
                ((get_page_url(p), p) for p in pagedict.values())
        )
        changes = []

        # if the cache exists: check whether the file has been updated
        if self.cache:
          pages_dict=self.cache.get_changed_pages(pages_dict,existing_pages)

        # sort by key (url_path) so we can create in right order
        for url_path in sorted(pages_dict.keys()):
            self._print('Processing: %s' % url_path)
            v = pages_dict[url_path]
            content_struct = dict(v)
            if url_path.startswith('/'):
                url_path = url_path[1:]
            if url_path.endswith('/'):
                url_path = url_path[:-1]
            segments = url_path.split('/')
            content_struct['wp_slug'] = segments[-1]
            if len(segments) > 1:
                # must either already exist of have been created
                parent_url_path = '/'.join(segments[:-1])
                parent_page_id = existing_pages[parent_url_path]['page_id']
                content_struct['wp_page_parent_id'] = parent_page_id

            if not url_path in existing_pages:
                page_id = self.new_page(**content_struct)
                existing_pages[url_path] = { 'page_id': page_id }
                changes.append([url_path, page_id, 'new'])
            else:
                page_id = existing_pages[url_path]['page_id']
                self.edit_page(page_id, **content_struct)
                changes.append([url_path, page_id, 'edited'])
            if self.delay:
                import time
                time.sleep(self.delay)
        return changes


def _object_methods(obj):
    methods = inspect.getmembers(obj, inspect.ismethod)
    methods = [name_y for name_y in methods if not name_y[0].startswith('_')]
    methods = dict(methods)
    return methods


def main(sysargs=sys.argv[:]):
    _methods = _object_methods(Wordpress)
    usage = '''%prog {action}

Actions:

    '''
    wpusage = '\n    '.join([
        '%s: %s' % (name, m.__doc__.split('\n')[0] if m.__doc__ else '')
        for (name, m) in sorted(_methods.items())
    ])
    usage += wpusage

    parser = optparse.OptionParser(usage)
    parser.add_option('-c', '--config',
            help='configuration file to use (e.g. for wordpress config)',
            default='config.ini')
    options, args = parser.parse_args(sysargs[1:])

    if not args or not args[0] in _methods:
        parser.print_help()
        return 1

    action = args[0] 
    wordpress = Wordpress.init_from_config(options.config)
    wordpress.verbose = True
    out = getattr(wordpress, action)(*args[1:])
    if out:
        pprint.pprint(out)

    return 0


if __name__ == '__main__':
    sys.exit(main())
