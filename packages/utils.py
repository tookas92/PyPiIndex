import json

import markdown

from packages.documents import PackageDocument


class PackageDocumentParser:
    def __call__(self, document: PackageDocument) -> PackageDocument:
        self.document = document
        self._parse_downloads()
        self._parse_classifiers()
        self._parse_description()
        self._parse_releases()

        return self.document

    def _parse_classifiers(self):
        if self.document.classifiers:
            self.document.classifiers = self.document.classifiers.split(",")

    def _parse_downloads(self):
        downloads = json.loads(self.document.downloads)
        downloads_mapping = {
            "last_day": "Last day",
            "last_week": "Last week",
            "last_month": "Last month",
        }
        self.document.downloads = [
            f"{downloads_mapping[k]}: {v if v != -1 else 0}"
            for k, v in downloads.items()
        ]

    def _parse_description(self):
        # TODO parsowanie wg content_type description (są opisy w markdown bez ct, zdarzają się inne formatowania, ale raczej nie w nowych paczkach)
        md = markdown.Markdown()
        self.document.description = md.convert(self.document.description)

    def _parse_releases(self):
        releases_dict = {}
        if self.document.releases:
            releases = json.loads(self.document.releases)
            for version, data in releases.items():
                releases_dict[version] = data[0].get("url")

            self.document.releases = releases_dict


parse_package_document = PackageDocumentParser()
