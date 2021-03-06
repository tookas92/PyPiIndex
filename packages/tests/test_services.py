from unittest.mock import Mock

from django.test import TestCase
from requests.exceptions import RequestException

from packages.documents import PackageDocument
from packages.models import Package
from packages.services import (APIChangedError, PyPiPackagesAdapter,
                               PyPiPackagesProcessor)


class TestPyPiPackagesAdapter(TestCase):
    def setUp(self):
        self.transport = Mock()
        self.transport.get.return_value.status_code = 200
        self.xml = """
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

    def test_get_packages(self):

        expected_output = ["patch-env"]
        self.transport.get.return_value.content = self.xml

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package = adapter.get_packages_names()
        self.assertEqual(package, expected_output)

    def test_get_packages_names_request_error_returns_empty_list(self):
        expected_output = []
        self.transport.get.side_effect = RequestException

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
        expected_json = '{"test": "json"}'
        expected_output = [expected_json]
        self.transport.get.return_value.content = self.xml
        self.transport.get.return_value.json.return_value = expected_json

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package_names = adapter.get_packages_names()
        package_jsons = adapter.get_packages_json_list(package_names)

        self.assertEqual(package_jsons, expected_output)

    def test_get_packages_json_list_request_error(self):
        expected_output = []
        self.transport.get.side_effect = RequestException

        adapter = PyPiPackagesAdapter(transport=self.transport)
        package_names = adapter.get_packages_names()
        package_jsons = adapter.get_packages_json_list(package_names)

        self.assertEqual(package_jsons, expected_output)


class TestPyPiPackagesProcessor(TestCase):
    def setUp(self):
        self.return_val = [
            {
                "info": {
                    "author": "Test Test",
                    "author_email": "kehillio@pasteur.fr",
                    "bugtrack_url": None,
                    "classifiers": [],
                    "description": "",
                    "description_content_type": "",
                    "docs_url": None,
                    "download_url": "",
                    "downloads": {"last_day": -1, "last_month": -1, "last_week": -1},
                    "home_page": "",
                    "keywords": "",
                    "license": "",
                    "maintainer": "",
                    "maintainer_email": "",
                    "name": "dabeplech",
                    "package_url": "https://pypi.org/project/dabeplech/",
                    "platform": "",
                    "project_url": "https://pypi.org/project/dabeplech/",
                    "project_urls": None,
                    "release_url": "https://pypi.org/project/dabeplech/0.0.5/",
                    "requires_dist": [
                        "pydantic (==1.5.1)",
                        "requests (==2.23.0)",
                        "colored (==1.4.2)",
                    ],
                    "requires_python": "",
                    "summary": "Light library to perform request to different bioinformatics APIs",
                    "version": "0.0.5",
                    "yanked": False,
                    "yanked_reason": None,
                },
            }
        ]

    def test_index_packages(self):
        adapter_mock = Mock()
        adapter_mock.get_packages_json_list.return_value = self.return_val

        proc = PyPiPackagesProcessor(adapter=adapter_mock)
        proc.index_packages()
        package_cnt = Package.objects.count()
        # document_cnt = PackageDocument.search().query('match', author="Test Test").count()
        #
        # self.assertEqual(document_cnt, 1)
        self.assertEqual(package_cnt, 1)

    def test_index_packages_api_changed(self):
        adapter_mock = Mock()
        self.return_val[0]["info"].pop("license")
        adapter_mock.get_packages_json_list.return_value = self.return_val

        proc = PyPiPackagesProcessor(adapter=adapter_mock)

        with self.assertRaises(APIChangedError):
            proc.index_packages()
