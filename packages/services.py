import requests
import xmltodict

from collections import OrderedDict


class PyPiPackagesAdapter:
    PYPI_PACKAGES_URL = "https://pypi.org/rss/packages.xml"
    PYPI_JSON_API_URL = "https://pypi.org/pypi/{}/json"

    def __init__(self, transport=requests):
        self.transport = transport

    def _get_packages_xml(self):
        response = self.transport.get(self.PYPI_PACKAGES_URL)
        return response.content

    def _transform_xml_to_dict(self):
        packages_xml = self._get_packages_xml()
        packages_dict = xmltodict.parse(packages_xml)
        return packages_dict

    def _get_updated_packages_list(self):
        try:
            return self._transform_xml_to_dict()["rss"]["channel"]["item"]
        except KeyError:
            return []

    def get_packages_names(self):
        packages = self._get_updated_packages_list()
        if packages and type(packages) == list:
            return [package.get("link").split("/")[-2] for package in packages]
        elif packages and type(packages) == OrderedDict:
            return [packages.get("link").split("/")[-2]]
        else:
            return []

    def get_packages_json_list(self, packages_list):
        json_list = []
        for name in packages_list:
            resp = self.transport.get(self.PYPI_JSON_API_URL.format(name))
            json_list.append(resp.json())
        return json_list
