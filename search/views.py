import math
import json
import markdown

from django.http import HttpResponse
from django.conf import settings
from django.views import View
from django.shortcuts import render
from elasticsearch_dsl import Q

from packages.documents import PackageDocument

# Create your views here.


class SearchView(View):
    def get(self, request):
        curr_page = int(request.GET.get("page", 1))
        search_param = request.GET.get("search")

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

        total = search.count()
        total_pages = math.ceil(total / settings.ELASTICSEARCH_PAGINATE_BY) + 1
        offset = (curr_page - 1) * settings.ELASTICSEARCH_PAGINATE_BY
        limit = offset + settings.ELASTICSEARCH_PAGINATE_BY
        search = search[offset:limit]
        results = search.execute()

        ctx = {
            "packages": results,
            "pages": range(1, total_pages),
            "curr_page": curr_page,
            "total_pages": total_pages,
            "total_cnt": total
        }
        return render(request, "index.html", context=ctx)

def parse_classifiers(classifiers):
    return classifiers.split(',')


class PackageDocumentDetailView(View):

    def get(self, request, id):
        document = PackageDocument.get(id=id)
        md = markdown.Markdown()
        document.description = md.convert(document.description)
        document.classifiers = parse_classifiers(document.classifiers)

        ctx = {"package": document}
        return render(request, "detail.html", context=ctx)
