from django_elasticsearch_dsl import Document, Index, fields

from packages.models import Package

package_index = Index("packages")


package_index.settings(number_of_shards=1, number_of_replicas=0)


@package_index.document
class PackageDocument(Document):
    class Django:
        model = Package
        fields = [
            "id",
            "author",
            "author_email",
            "bugtrack_url",
            "classifiers",
            "description",
            "description_content_type",
            "docs_url",
            "download_url",
            "downloads",
            "home_page",
            "keywords",
            "license",
            "maintainer",
            "maintainer_email",
            "name",
            "package_url",
            "platform",
            "project_url",
            "project_urls",
            "release_url",
            "requires_dist",
            "requires_python",
            "summary",
            "version",
            "yanked",
            "yanked_reason",
            "releases",
        ]
