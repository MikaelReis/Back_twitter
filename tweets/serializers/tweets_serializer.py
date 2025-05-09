from rest_framework import serializers
from tweets.models import Tweets
from tweets.models import Comments

class TweetsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweets
        fields = ['id', 'user', 'username', 'content', 'created_at', 'likes_count', 'is_liked', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(id=user.id).exists() if user.is_authenticated else False
        
    def get_comments_count(self, obj):
        return obj.comments.count()
    
class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'content', 'user', 'created_at', 'username']

    def get_username(self, obj):
        return obj.user.username

