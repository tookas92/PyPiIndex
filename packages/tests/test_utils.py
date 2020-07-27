from django.test import TestCase
from elasticsearch_dsl.utils import AttrList

from packages.documents import PackageDocument
from packages.utils import parse_package_document


class TestParsePackageDocument(TestCase):
    def setUp(self):
        self.description = "* [AngularJS] - HTML enhanced for web apps!"
        self.classifiers = "Programming Language :: Python :: 3,Programming Language :: Python :: 3.6"
        self.downloads = '{"last_day": -1, "last_week": -1, "last_month": -1}'
        self.releases = '{"0.1": [{"digest": "xxxxx", "url": "http://url.test"}]}'

    def test_parse_package_document(self):
        document = PackageDocument(
            description=self.description,
            classifiers=self.classifiers,
            downloads=self.downloads,
            releases=self.releases
        )
        expected_downloads = ["Last day: 0", "Last week: 0", "Last month: 0"]
        expected_classifiers = AttrList([
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
        ])
        expected_description = (
            "<ul>\n<li>[AngularJS] - HTML enhanced for web apps!</li>\n</ul>"
        )
        expected_releases = {"0.1": "http://url.test"}

        document = parse_package_document(document)

        self.assertEqual(document.downloads, expected_downloads)
        self.assertEqual(document.description, expected_description)
        self.assertEqual(document.releases.to_dict(), expected_releases)
        self.assertEqual(document.classifiers, expected_classifiers)

    def test_parse_releases_changed_format_handles_exceptions(self):
        self.releases = '{"0.1": {"digest": "xxxxx", "url": "http://url.test"}}'
        document = PackageDocument(releases=self.releases, description='')

        document = parse_package_document(document)

        self.assertEqual(document.releases, {})

