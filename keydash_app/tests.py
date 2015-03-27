from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from keydash_app.models import Game, UserProfile, Score
from django.http import HttpResponseRedirect
from keydash_app.views import game_mode_readable_name
import  datetime
import json



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

def add_games(game_mode, game_js, game_css):
    game = Game.objects.get_or_create(game_mode=game_mode,
                                      game_js=game_js,
                                      game_css=game_css)[0]
    return game

def add_score(user, game, wpm, accuracy, score, date):
    score = Score.objects.get_or_create(user=user,
                                        game=game,
                                        wpm=wpm,
                                        accuracy=accuracy,
                                        score=score,
                                        date=date)[0]
    return score


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



class UserProfileModelTests(TestCase):

    def setUp(self):
        self.user = add_user('Gummo','gummo@gmail.com','gummo')
        self.profile = add_user_profile(self.user, 1, 100, 100, 1000)


    def test_user_profile(self):
        self.assertEquals(self.profile.user, self.user)



class ScoreModelTests(TestCase):

    def setUp(self):
        self.user = add_user('Gummo','gummo@gmail.com','gummo')
        self.game = add_games('eng_dict', 'textgame.js', 'textgame.css')
        self.score = add_score(self.user, self.game, 100, 100, 10000, datetime.datetime(2015,3,16,23,30))


    def test_score(self):
        self.assertEquals(self.score.user, self.user)
        self.assertEquals(self.score.game, self.game)


class PersonalStatisticsTest(TestCase):

    def setUp(self):
        self.user = add_user('Gummo','gummo@gmail.com','gummo')
        self.profile = add_user_profile(self.user, 1, 100, 100, 1000)
        self.game = add_games('eng_dict', 'textgame.js', 'textgame.css')
        self.game2 = add_games('rand_alpha', 'textgame.js', 'textgame.css')
        self.score = add_score(self.user, self.game, 100, 90, 9000, datetime.datetime(2015,3,16,23,30))
        self.score = add_score(self.user, self.game, 100, 100, 10000, datetime.datetime(2015,3,17,23,30))
        self.score = add_score(self.user, self.game, 100, 80, 8000, datetime.datetime(2015,3,18,23,30))
        self.score = add_score(self.user, self.game2, 100, 70, 7000, datetime.datetime(2015,3,19,23,30))



    def test_best_scores(self):
        self.client.login(username='Gummo', password='gummo')
        response = self.client.get(reverse('statistics_personal'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "9000")

        number_of_scores =len(response.context['scores'])
        self.assertEqual(number_of_scores, 4)

        response = self.client.post(reverse('statistics_personal'), {'dropdown_game_mode': 'eng_dict'})
        self.assertContains(response, 'English Dictionary')
        number_of_scores_dropdown_table =len(response.context['user_scores_for_game_mode'])
        self.assertEqual(number_of_scores_dropdown_table, 3)


class GlobalStatisticsTest(TestCase):

    def setUp(self):
        self.user = add_user('Gummo','gummo@gmail.com','gummo')
        self.user2 = add_user('Gummo2','gummo2@gmail.com','gummo2')
        self.profile = add_user_profile(self.user, 1, 100, 100, 10000)
        self.profile2 = add_user_profile(self.user2, 2, 100, 100, 20000)
        self.game = add_games('eng_dict', 'textgame.js', 'textgame.css')
        self.game2 = add_games('rand_alpha', 'textgame.js', 'textgame.css')
        self.score = add_score(self.user, self.game, 100, 90, 9000, datetime.datetime(2015,3,16,23,30))
        self.score = add_score(self.user2, self.game, 100, 100, 10000, datetime.datetime(2015,3,17,23,30))
        self.score = add_score(self.user, self.game2, 100, 80, 8000, datetime.datetime(2015,3,18,23,30))
        self.score = add_score(self.user2, self.game2, 100, 70, 7000, datetime.datetime(2015,3,19,23,30))


    def test_global_best_scores(self):
        self.client.login(username='Gummo', password='gummo')
        response = self.client.get(reverse('statistics_global'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10000")

        statistics_users = len(response.context['users'])
        self.assertEqual(statistics_users, 2)

        response = self.client.post(reverse('statistics_global'),{'dropdown_game_mode': 'eng_dict'})
        self.assertContains(response, 'English Dictionary')
        number_of_scores_dropdown_table =len(response.context['user_scores_for_game_mode'])
        self.assertEqual(number_of_scores_dropdown_table, 2)


class GameModeReadableNameTest(TestCase):
    def setUp(self):
        self.game1 = add_games('eng_dict', 'textgame.js', 'textgame.css')
        self.game2 = add_games('rand_alpha', 'textgame.js', 'textgame.css')
        self.game3 = add_games('rand_alpha_punc', 'textgame.js', 'textgame.css')
        self.game4 = add_games('paragraph', 'textgame.js', 'textgame.css')
        self.game5 = add_games('typingflight', 'gameframework.js,spriteengine.js,typingflight.js', 'typingflight.css')



    def test_game_mode_readable_name(self):
        self.assertEqual(game_mode_readable_name(self.game1)['game_mode'],'English Dictionary')
        self.assertEqual(game_mode_readable_name(self.game2)['game_mode'],'Random Alphanumeric')
        self.assertEqual(game_mode_readable_name(self.game3)['game_mode'],'Random Alphanumeric + Punctuation')
        self.assertEqual(game_mode_readable_name(self.game4)['game_mode'],'Paragraph')
        self.assertEqual(game_mode_readable_name(self.game5)['game_mode'],'Typing Flight')