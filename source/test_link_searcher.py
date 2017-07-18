import unittest
from links_searcher import LinksSearcher
import operator


class TestUM(unittest.TestCase):
    """
    Test for LinkSearcher
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        links = LinksSearcher('segawg ст 154 жк рф ывпрыр').get_simple_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].link_text, 'ст 154 жк рф')
        self.assertEqual(links[0].article_num, '154')
        self.assertEqual(links[0].law_name, 'жк')

        links = LinksSearcher('38476 трололо статья 159  ук рф кееек ывп ст. 209 гк рф').get_simple_links()
        links = sorted(links,  key=operator.attrgetter('link_text'))
        self.assertEqual(len(links), 2)
        self.assertEqual(links[1].link_text, 'статья 159  ук рф')
        self.assertEqual(links[0].link_text, 'ст. 209 гк рф')

        links = LinksSearcher('segawg п. 1. ст. 162 гк рф ывпр гк рф статья 578. ыр').get_simple_links()
        links = sorted(links, key=operator.attrgetter('link_text'))
        self.assertEqual(len(links), 2)
        self.assertEqual(links[1].link_text, 'п. 1. ст. 162 гк рф')
        self.assertEqual(links[0].link_text, 'гк рф статья 578')

        links = LinksSearcher('ст.209 ГК ывпрыр').get_simple_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].link_text, 'ст.209 гк')

        links = LinksSearcher('часть 1 ст. 51 жк рф ывпрыр 1 ч. ст. 51 жк рф').get_simple_links()
        links = sorted(links,  key=operator.attrgetter('link_text'))
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].law_name, 'жк')

        links = LinksSearcher('ст. 25 ФЗ "О защите прав потребителей".  ').get_simple_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].link_text, 'ст. 25 фз "о защите прав потребителей"')

        links = LinksSearcher('ст. 25 ФЗ №3586').get_simple_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].link_text, 'ст. 25 фз №3586')

        links = LinksSearcher('трололо гк российской федерации п. 1 ст. 25 кек кек кек').get_simple_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].link_text, 'гк российской федерации п. 1 ст. 25')
# ст.209 ГК

if __name__ == '__main__':
    unittest.main()