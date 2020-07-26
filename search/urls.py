from django.urls import path

from search.views import PackageDocumentDetailView, SearchView

urlpatterns = [
    path("", SearchView.as_view()),
    path("package/<id>/", PackageDocumentDetailView.as_view()),
]
