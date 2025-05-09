from django.urls import path, include
from rest_framework import routers
from follows.viewsets import FollowsViewSet

router = routers.SimpleRouter()
router.register(r'', FollowsViewSet, basename="follows")

urlpatterns = [
    path("", include(router.urls)),
]