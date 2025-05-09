import factory

from tweets.models import Tweets
from users.factories import UsersFactory

class TweetsFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UsersFactory)
    content = factory.Faker("sentence")

    class Meta:
        model = Tweets