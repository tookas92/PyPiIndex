from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from packages.documents import PackageDocument


class PackageDocumentSerializer(DocumentSerializer):
    class Meta:
        document = PackageDocument
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
