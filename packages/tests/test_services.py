from collections import OrderedDict

from django.test import TestCase
from unittest.mock import Mock, patch

from packages.services import PyPiPackagesAdapter


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
        expected_output = ["patch-env"]
        self.transport.get.return_value.content = xml

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package = adapter.get_packages_names()
        self.assertEqual(package, expected_output)

    def test_empty_list_if_no_packages(self):
        xml = """
            <rss version="2.0">
            </rss>
        """
        self.transport.get.return_value.content = xml

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package = adapter.get_packages_names()

        self.assertEqual(package, [])

    def test_get_packages_json_list(self):
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
        expected_json = '{"test": "json"}'
        expected_output = [expected_json]
        self.transport.get.return_value.content = xml
        self.transport.get.return_value.json.return_value = expected_json

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package_names = adapter.get_packages_names()
        package_jsons = adapter.get_packages_json_list(package_names)

        self.assertEqual(package_jsons, expected_output)
