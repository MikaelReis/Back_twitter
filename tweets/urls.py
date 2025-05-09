from django.urls import path, include
from rest_framework import routers
from tweets.viewsets import TweetsViewSet
from tweets.viewsets import CommentsViewSet

router = routers.SimpleRouter()
router.register(r'', TweetsViewSet, basename="tweets")

tweets_with_comments = [
    path('<int:tweet_id>/comments/', CommentsViewSet.as_view({'get': 'list', 'post': 'create'}), name='tweet-comments-list'),
    path('<int:tweet_id>/comments/<int:pk>/', CommentsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='tweet-comments-detail'),
]

urlpatterns = [
    path("", include(router.urls)),
    path("", include(tweets_with_comments)),
]