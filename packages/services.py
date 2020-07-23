import requests
import xmltodict
import json

from collections import OrderedDict


from packages.models import Package


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


def index_packages():
    adapter = PyPiPackagesAdapter()
    names = adapter.get_packages_names()
    json_list = adapter.get_packages_json_list(names)
    for data_ob in json_list:
        data = data_ob.get('info')
        Package.objects.create(
            author=data['author'],
            author_email=data['author_email'],
            bugtrack_url=data['bugtrack_url'],
            classifiers=','.join(data['classifiers']) if data.get('classifiers') else '',
            description=data['description'],
            description_content_type=data['description_content_type'],
            docs_url=data['docs_url'],
            download_url=data['download_url'],
            downloads=json.dumps(data['downloads']),
            home_page=data['home_page'],
            keywords=data['keywords'],
            license=data['license'],
            maintainer=data['maintainer'],
            maintainer_email=data['maintainer_email'],
            name=data['name'],
            package_url=data['package_url'],
            platform=data['platform'],
            project_url=data['project_url'],
            project_urls=json.dumps(data['project_urls']),
            release_url=data['release_url'],
            requires_dist=','.join(data['requires_dist']) if data.get('requires_dist') else '',
            requires_python=data['requires_python'],
            summary=data['summary'],
            version=data['version'],
            yanked=data['yanked'],
            yanked_reason=data['yanked_reason'],
            releases=json.dumps(data['releases']) if data.get('releases') else ''
        )


class PyPiPackagesProcessor:

    def __init__(self, adapter=PyPiPackagesAdapter()):
        self.adapter = adapter

    def _prepare_json_list(self):
        names = self.adapter.get_packages_names()
        return self.adapter.get_packages_json_list(names)

    def index_packages(self):
        json_list = self._prepare_json_list()

        for data_obj in json_list:
            data = data_obj.get('info')

            obj, created = Package.objects.update_or_create(
                author=data['author'],
                author_email=data['author_email'],
                name=data['name'],
                defaults=dict(
                    bugtrack_url=data['bugtrack_url'],
                    classifiers=','.join(data['classifiers']) if data.get('classifiers') else '',
                    description=data['description'],
                    description_content_type=data['description_content_type'],
                    docs_url=data['docs_url'],
                    download_url=data['download_url'],
                    downloads=json.dumps(data['downloads']),
                    home_page=data['home_page'],
                    keywords=data['keywords'],
                    license=data['license'],
                    maintainer=data['maintainer'],
                    maintainer_email=data['maintainer_email'],
                    package_url=data['package_url'],
                    platform=data['platform'],
                    project_url=data['project_url'],
                    project_urls=json.dumps(data['project_urls']),
                    release_url=data['release_url'],
                    requires_dist=','.join(data['requires_dist']) if data.get('requires_dist') else '',
                    requires_python=data['requires_python'],
                    summary=data['summary'],
                    version=data['version'],
                    yanked=data['yanked'],
                    yanked_reason=data['yanked_reason'],
                    releases=json.dumps(data['releases']) if data.get('releases') else ''
                )
            )

