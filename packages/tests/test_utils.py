from django.test import TestCase

from packages.utils import parse_package_document
from packages.documents import PackageDocument


class TestParsePackageDocument(TestCase):

    def test_parse_package_document(self):
        document = PackageDocument(
            description='* [AngularJS] - HTML enhanced for web apps!',
            classifiers='Programming Language :: Python :: 3, Programming Language :: Python :: 3.6',
            downloads='{"last_day": -1, "last_week": -1, "last_month": -1}'
        )
        expected_downloads = ["Last day: 0", "Last week: 0", "Last month: 0"]
        expected_classifiers = ["Programming Language :: Python :: 3", "Programming Language :: Python :: 3.6"]
        expected_description = '<ul>\n<li>[AngularJS] - HTML enhanced for web apps!</li>\n</ul>'

        document = parse_package_document(document)

        self.assertEqual(document.downloads, expected_downloads)
        self.assertEqual(document.classifiers[0], expected_classifiers[0])
        self.assertEqual(document.description, expected_description)