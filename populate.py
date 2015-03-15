import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keydash_project.settings')

import django
django.setup()

from keydash_app.models import UserProfile, Game, Score
from django.contrib.auth.models import User

def populate():
    user = add_user('groucho','groucho@gmail.com','groucho')
    add_user_profile(user, 1, 100, 100, 1000)
    user = add_user('harpo','harpo@gmail.com','harpo')
    add_user_profile(user, 2, 90, 90, 900)
    user = add_user('chico','chico@gmail.com','chico')
    add_user_profile(user, 3, 80, 80, 800)
    user = add_user('zeppo','zeppo@gmail.com','zeppo')
    add_user_profile(user, 4, 70, 70, 700)


def add_user(username, email, password):
    user = User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(password)
    user.save()
    return user

def add_user_profile(user, ranking_position, wpm_highest, accuracy_highest, score_highest):
    userprofile = UserProfile.objects.get_or_create(user=user,
                                                    ranking_position=ranking_position,
                                                    wpm_highest=wpm_highest,
                                                    accuracy_highest=accuracy_highest,
                                                    score_highest = score_highest)[0]
    return userprofile

if __name__ == '__main__':
    print "Starting Keydash population script..."
    populate()