import math

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views import View
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Q
from urllib3.exceptions import ConnectionError

from packages.documents import PackageDocument
from packages.utils import parse_package_document

# Create your views here.


class SearchView(View):
    def get(self, request):
        curr_page = int(request.GET.get("page", 1))
        search_param = request.GET.get("search")
        paginate_by = settings.ELASTICSEARCH_PAGINATE_BY

        search = PackageDocument.search()

        if search_param:
            query = Q(
                "multi_match",
                query=search_param,
                fields=[
                    "name",
                    "author",
                    "author_email",
                    "description",
                    "keywords",
                    "version",
                    "maintainer",
                    "maintainer_email",
                ],
            )
            search = search.query(query)
        try:
            total = search.count()
            total_pages = math.ceil(total / paginate_by)
            offset = (curr_page - 1) * paginate_by
            limit = offset + paginate_by
            search = search[offset:limit]
            results = search.execute()

            ctx = {
                "packages": results,
                "pages": range(1, total_pages),
                "curr_page": curr_page,
                "total_pages": total_pages,
                "total_cnt": total,
            }
        except ConnectionError as e:
            print(e)
            ctx = {"error": "Something went wrong. Contact with administrator."}

        return render(request, "index.html", context=ctx)


class PackageDocumentDetailView(View):
    def get(self, request, id):
        try:
            document = PackageDocument.get(id=id)
            document = parse_package_document(document)
            ctx = {"package": document}
        except NotFoundError as e:
            raise Http404("Package does not exist")

        return render(request, "detail.html", context=ctx)
