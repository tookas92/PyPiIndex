from django_elasticsearch_dsl import Document, fields, Index

from packages.models import Package

package_index = Index('packages')


package_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@package_index.document
class PackageDocument(Document):

    class Django:
        model = Package
