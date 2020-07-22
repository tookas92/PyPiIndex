from collections import OrderedDict

from django.test import TestCase
from unittest.mock import Mock, patch

from pypiindex.packages.services import PyPiPackagesAdapter

class TestPyPiPackagesAdapter(TestCase):

    def setUp(self):
        self.transport = Mock()

    def test_get_packages(self):
        xml = """
            <rss version="2.0">
                <channel>
                    <item>
                        <title>patch-env added to PyPI</title>
                        <link>https://pypi.org/project/patch-env/</link>
                        <guid>https://pypi.org/project/patch-env/</guid>
                        <description>
                        Patch os.environ with dynamic values when the interpreter starts
                        </description>
                        <author>info@caricalabs.com</author>
                        <pubDate>Wed, 22 Jul 2020 19:09:42 GMT</pubDate>
                    </item>
                </channel>
            </rss>
        """
        expected_dict = OrderedDict(
            title='patch-env added to PyPI',
            link='https://pypi.org/project/patch-env/',
            guid='https://pypi.org/project/patch-env/',
            description='Patch os.environ with dynamic values when the interpreter starts',
            author='info@caricalabs.com',
            pubDate='Wed, 22 Jul 2020 19:09:42 GMT'
        )
        self.transport.get.return_value.content = xml

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package = adapter.get_packages_list()

        self.assertEqual(package, expected_dict)

    def test_empty_list_if_no_packages(self):
        xml = """
            <rss version="2.0">
            </rss>
        """
        self.transport.get.return_value.content = xml

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package = adapter.get_packages_list()

        self.assertEqual(package, [])

