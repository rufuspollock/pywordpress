import unittest

import pywordpress


class TestWordpress(unittest.TestCase):
    _pages_to_cleanup = ()

    def setUp(self):
        self.wordpress = pywordpress.Wordpress.init_from_config('test.ini')
        self._pages_to_cleanup = []

    def tearDown(self):
        for page_id in self._pages_to_cleanup:
            self.wordpress.delete_page(page_id)

    def test_01_all(self):
        w = self.wordpress
        # get_pages and get_page_list differ in their treatment of deleted (in
        # trash) pages. Former does not return them, latter does ...
        pages_start = w.get_pages()

        title = 'test title'
        content = 'test content, from python'
        new_page_id = w.new_page(title=title, description=content)
        self._pages_to_cleanup.append(new_page_id)
        assert new_page_id > 0

        pages = w.get_pages()
        assert len(pages) == len(pages_start) + 1, (pages, pages_start)
        page = w.get_page(new_page_id)
        assert page['title'] == title, page
        assert page['description'] == content, page

        new_title = 'test title updated'
        edited = w.edit_page(new_page_id, title=new_title)
        assert edited
        page = w.get_page(new_page_id)
        assert page['title'] == new_title, page
        assert page['description'] == content, page

        deleted = w.delete_page(new_page_id)
        pages = w.get_pages()
        pages2 = w.get_page_list()
        # see above re difference in set of pages returned
        assert pages != pages2, (len(pages), len(pages2))
        assert len(pages) == len(pages_start), (pages, pages_start)

    def test_02_create_many_pages(self):
        self.skipTest('Something is wrong with transactions or huh?')
        url1 = '/testpage/'
        url2 = url1 + 'subpage'

        # assumes this test suite is the only thing creating pages 
        # during the test run
        total_expected_n_pages = 2 + len(self.wordpress.get_page_list())

        pages_dict = {
            url1: {
                'title': 'Test Page',
                'description': 'xxx'
            },
            url2: {
                'title': 'ABC',
                'description': 'subpage xxx'
            }
        }

        changes = self.wordpress.create_many_pages(pages_dict)
        for _, page_id, _ in changes:
            self._pages_to_cleanup.append(page_id)

        def _check(which):
            pages = dict(
                [(p['page_id'], p) for p in self.wordpress.get_page_list()]
            )
            # FIXME `get_pages` returns different results than `get_page_list`
            assert len(pages) == total_expected_n_pages, (
                '{0} check, expected len(pages) == {1!r}, '
                'but len(pages) is {2!r}').format(
                    which, total_expected_n_pages, len(pages)
                )
            testpage = pages_dict[url1]
            outtestpage = pages[testpage['title']]
            assert outtestpage['description'] == \
                testpage['description'], '{0} {1!r}'.format(which, outtestpage)

            subpage = pages_dict[url2]
            assert pages[subpage['title']]['title'] == subpage['title'], \
                    '{0} check, title of subpage: {1!r}'.format(which, subpage)

        _check('1st')

        # now repeat to check we edit rather than create
        changes = self.wordpress.create_many_pages(pages_dict)
        for _, page_id, _ in changes:
            self._pages_to_cleanup.append(page_id)

        assert len(changes) == 2, '2 changes completed: {0!r}'.format(changes)

        _check('2nd')
        assert [change[2] for change in changes] == 2 * ['edited'], changes


def test():
    unittest.main()

