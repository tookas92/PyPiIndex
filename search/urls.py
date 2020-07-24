from django.urls import path

from search.views import SearchView, PackageDocumentDetailView

urlpatterns = [
    path("", SearchView.as_view()),
    path("package/<id>/", PackageDocumentDetailView.as_view())
]
