from django.db import models
from django.conf import settings

class Tweets(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tweets'
    )
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_tweets',
        blank=True
    )

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'

class Comments (models.Model):
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} comentou: {self.content[:30]}'
