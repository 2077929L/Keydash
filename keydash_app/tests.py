from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from keydash_app.models import Game, UserProfile
from django.http import HttpResponseRedirect
import json

# Create your tests here.
class WordAPITests(TestCase):
    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    #a valid request should get a sjaon response with a list of words
    def test_request_new_words(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('game_get_new_data', kwargs={'game_mode': 'eng_dict'}))
        #response is json?
        self.assertEqual(response['Content-Type'], "application/json")
        #response contains words?
        self.assertContains(response, 'words')


    #requests without login should redirect as the game cannot run without login
    def test_request_new_words_no_login(self):
        response = self.client.get(reverse('game_get_new_data', kwargs={'game_mode': 'eng_dict'}))
        #response is redirect?
        self.assertTrue(isinstance(response, HttpResponseRedirect))


class ScoreSubmitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        userprofile = UserProfile.objects.get_or_create(user=self.user,
                                                        ranking_position=5,
                                                        wpm_highest=0,
                                                        accuracy_highest=0,
                                                        score_highest = 0)[0]
        game = Game.objects.get_or_create(game_mode='testgame',
                                          game_js='game_js',
                                          game_css='game_css')


    def test_save_score(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('game_add_new_score'), {'game_type': 'testgame', 'wpm': 120, 'accuracy': 98})
        self.assertContains(response, '"success": "true"')
        userprofile = UserProfile.objects.get_or_create(user=self.user)[0]
        #check userprofile was updated
        self.assertEqual(userprofile.accuracy_highest, 98)
        self.assertEqual(userprofile.wpm_highest, 120)
        self.assertEqual(userprofile.ranking_position, 1)

    def test_save_score_no_login(self):
        response = self.client.post(reverse('game_add_new_score'), {'game_type': 'testgame', 'wpm': 120, 'accuracy': 98})
        self.assertTrue(isinstance(response, HttpResponseRedirect))


class UserRegistration(TestCase):
    def test_valid_registration(self):
        response = self.client.post('/accounts/register/', {'username': 'testuser', 'email': 'user@user.com', 'password1': 'passtest', 'password2': 'passtest'})
        #check we got a redirect to profile creation
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        response = self.client.get(reverse('add_profile'))
        #redirect to profile page
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        try:
            user = User.objects.get(username='testuser')
        except User.DoesNotExist:
            user = None
        #user was created    
        self.assertTrue(user != None)

        try:
            userprofile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            userprofile = None
        #profile created
        self.assertTrue(userprofile != None)

        self.assertEqual(userprofile.picture, "profile_images/avatar.png")





