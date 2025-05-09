from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from tweets.models import Tweets, Comments
from tweets.serializers import TweetsSerializer, CommentsSerializer
from follows.models import Follows

class TweetsViewSet(viewsets.ModelViewSet):
    queryset = Tweets.objects.all().order_by('-created_at')
    serializer_class = TweetsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def following(self, request):
        following_ids = Follows.objects.filter(follower=request.user).values_list("following_id", flat=True)
        tweets = Tweets.objects.filter(user_id__in=following_ids).order_by("-created_at")
        serializer = self.get_serializer(tweets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        tweet = self.get_object()
        user = request.user
        if tweet.likes.filter(id=user.id).exists():
            tweet.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            tweet.likes.add(user)
            return Response({'status': 'liked'})
        
class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_id']
        return Comments.objects.filter(tweet_id=tweet_id).order_by('-created_at')

    def perform_create(self, serializer):
        tweet_id = self.kwargs.get("tweet_id")
        tweet = get_object_or_404(Tweets, id=tweet_id)
        serializer.save(user=self.request.user, tweet=tweet)