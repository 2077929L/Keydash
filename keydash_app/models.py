from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    ranking_position = models.IntegerField(default=0)
    # last_online = models.DateTimeField(default=datetime.now, blank=True) # DateField.auto_now
    wpm_highest = models.FloatField(default=0)
    accuracy_highest = models.FloatField(default=0)
    score_highest = models.IntegerField(default=0)

    # def get_friends(self):
    #     user = self.user
    #     return Friendship.objects.filter(Q(creator=user)|Q(friend=user))

    def __unicode__(self):
        return self.user.username


class Game(models.Model):
    game_mode = models.CharField(max_length=128)

    def __unicode__(self):
        return self.game_mode


class Score(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    wpm = models.FloatField(default=0)
    accuracy = models.FloatField(default=0)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.score)


# class Friendship(models.Model):
#     creator = models.ForeignKey(User, related_name="friendship_creator_set")
#     friend = models.ForeignKey(User, related_name="friend_set")
#     def __unicode__(self):
#         return str(self.creator) + ", " + str(self.friend)

class MonthlyWeatherByCity(models.Model):
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)
