import xmlrpc.client


class Wordpress(object):
    """Interact with an existing wordpress install via xml-rpc

    Sample usage::

        >>> from pywordpress import Wordpress
        >>> wp = Wordpress('http://wp.site.com/', 'my-username', 'my-password')
        >>> page_list = wp.get_page_list()
        ...
        >>> new_page_id = w.new_page(title='Title', description='Our content')
        >>> new_page = wp.get_page(new_page_id)
        >>> print new_page['title']
        Title
        >>> 
    """

    def __init__(self, wp_url, username, password, blog_id=0, verbose=False):
        self.user = username
        self.password = password
        self.wp_url = wp_url
        xmlrpc_url = wp_url.rstrip('/') + '/xmlrpc.php'
        self.server = xmlrpc.client.ServerProxy(xmlrpc_url)
        self.blog_id = blog_id
        self.verbose = verbose

    @classmethod
    def init_from_config(self, config_fp):
        """Class method to initialize a `Wordpress` instance from an ini file.

        For an example ini file see config.ini.tmpl
        """
        from configparser import ConfigParser
        cfg = ConfigParser()
        with open(config_fp) as infile:
            cfg.read_file(infile)

        wp_url = cfg.get('wordpress', 'url')
        wp_user = cfg.get('wordpress', 'user')
        wp_password = cfg.get('wordpress', 'password')
        return self(wp_url, wp_user, wp_password)

    def _print(self, msg):
        if self.verbose:
            print(msg)

    def get_page_list(self):
        """http://codex.wordpress.org/XML-RPC_wp#wp.getPageList"""
        results = self.server.wp.getPageList(
            self.blog_id,
            self.user,
            self.password
        )
        return results

    def get_page(self, page_id):
        """http://codex.wordpress.org/XML-RPC_wp#wp.getPage"""
        results = self.server.wp.getPage(
            self.blog_id,
            page_id,
            self.user,
            self.password
        )
        return results

    def get_pages(self):
        """http://codex.wordpress.org/XML-RPC_wp#wp.getPages"""
        results = self.server.wp.getPages(
            self.blog_id,
            self.user,
            self.password
        )
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
        """http://codex.wordpress.org/XML-RPC_wp#wp.newPage
        
        :param **kwargs: all other possible arguments for content struct (see
        WP docs).
        """
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
        """http://codex.wordpress.org/XML-RPC_wp#wp.deletePage"""
        result = self.server.wp.deletePage(
            self.blog_id,
            self.user,
            self.password,
            page_id
        )
        return bool(result)

    def delete_all_pages(self):
        """Delete all pages (i.e. delete_page for each page in instance).
        """
        for pagedict in self.get_page_list():
            self._print('Deleting: %s' % pagedict)
            self.delete_page(pagedict['page_id'])

    def edit_page(self, page_id, **kwargs):
        """http://codex.wordpress.org/XML-RPC_wp#wp.editPage

        Note: editing a page leads to a new revision.

        :param **kwargs: attribute values for content struct (see wordpress
                         docs).
        """
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
        return bool(result)

    def create_many_pages(self, pages_dict):
        """ Create many pages at once (and only create pages which do not
        already exist).

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
        """
        ## get a list of existing pages keyed by their urls

        ## use get_page_list as that shows trash items as well as active
        pagelist = [self.get_page(x['page_id']) for x in self.get_page_list()]
        pagedict = dict([ (p['page_id'], p) for p in pagelist ])

        def get_page_url(page):
            parent_id = page['wp_page_parent_id']
            if parent_id == 0:
                return page['wp_slug']
            else:
                return get_page_url(pagedict[parent_id]) + \
                        '/' + page['wp_slug']
        existing_pages = dict(
            [(get_page_url(p), p) for p in pagelist]
        )
        changes = []
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
        return changes

