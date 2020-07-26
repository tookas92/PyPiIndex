from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from api.serializers import PackageDocumentSerializer
from packages.documents import PackageDocument


class PackageViewSet(DocumentViewSet):
    document = PackageDocument
    serializer_class = PackageDocumentSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [
        SearchFilterBackend,
    ]

    search_fields = (
        "name",
        "author",
        "author_email",
        "description",
        "keywords",
        "version",
        "maintainer",
        "maintainer_email",
    )
