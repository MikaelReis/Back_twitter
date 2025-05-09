from django.urls import path, include
from rest_framework import routers
from users import  viewsets

router = routers.SimpleRouter()
router.register(r'', viewsets.UsersViewSet, basename="users") 

urlpatterns = [
    path("", include(router.urls)),
]
