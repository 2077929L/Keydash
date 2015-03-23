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
    game_js = models.CharField(max_length=512)
    game_css = models.CharField(max_length=512)

    def __unicode__(self):
        return self.game_mode


class Score(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    wpm = models.FloatField(default=0)
    accuracy = models.FloatField(default=0)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return str(self.score)
