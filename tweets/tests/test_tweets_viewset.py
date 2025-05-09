import pytest
from rest_framework.test import APIClient
from tweets.models import Tweets
from tweets.factories import TweetsFactory
from users.factories import UsersFactory
from follows.factories import FollowsFactory


@pytest.mark.django_db
class TestTweetViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = UsersFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_tweet(self):
        payload = {"content": "Meu primeiro tweet!"}
        response = self.client.post("/api/tweets/", payload)
        assert response.status_code == 201
        assert Tweets.objects.filter(user=self.user).count() == 1

    def test_list_tweets(self):
        TweetsFactory.create_batch(3)
        response = self.client.get("/api/tweets/")
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_detail_tweet(self):
        tweet = TweetsFactory()
        response = self.client.get(f"/api/tweets/{tweet.id}/")
        assert response.status_code == 200
        assert response.data["id"] == tweet.id

    def test_following_tweets(self):
        followed_user = UsersFactory()
        FollowsFactory(follower=self.user, following=followed_user)
        TweetsFactory(user=followed_user)
        TweetsFactory(user=self.user)

        response = self.client.get("/api/tweets/following/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["user"] == followed_user.id

    def test_like_tweet(self):
        tweet = TweetsFactory()
        response = self.client.post(f"/api/tweets/{tweet.id}/like/")
        assert response.status_code == 200
        assert response.data["status"] == "liked"

        response = self.client.post(f"/api/tweets/{tweet.id}/like/")
        assert response.status_code == 200
        assert response.data["status"] == "unliked"

    def test_create_comment(self):
        tweet = TweetsFactory()
        payload = {
            "content": "Comentando aqui!",
            "tweet": tweet.id,
        }
        response = self.client.post(f"/api/tweets/{tweet.id}/comments/", payload)
        assert response.status_code == 201