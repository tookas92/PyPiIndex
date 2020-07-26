from django.urls import include, path

urlpatterns = [path("", include("search.urls")), path("api/", include("api.urls"))]
