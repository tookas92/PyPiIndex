from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PackageViewSet

router = DefaultRouter()
router.register("packages", PackageViewSet, basename="packages")


urlpatterns = [path("", include(router.urls))]
