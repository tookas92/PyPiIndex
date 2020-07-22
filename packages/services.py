import requests
import xmltodict

class PyPiPackagesAdapter:
    PYPI_PACKAGES_URL = 'https://pypi.org/rss/packages.xml'

    def __init__(self, transport=requests):
        self.transport = transport

    def _get_packages_xml(self):
        response = self.transport.get(self.PYPI_PACKAGES_URL)
        return response.content

    def _get_packages_dict(self):
        packages_xml = self._get_packages_xml()
        packages_dict = xmltodict.parse(packages_xml)
        return packages_dict

    def get_packages_list(self):
        try:
            return self._get_packages_dict()['rss']['channel']['item']
        except KeyError:
            return []
