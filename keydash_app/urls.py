from django.conf.urls import patterns, url
from keydash_app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='front'),
        url(r'^home', views.index, name='home'),
        url(r'^about', views.about, name='about'),
        url(r'^trial', views.trial, name='trial'),
        url(r'^game/newwords/(?P<game_mode>[\w\-]+)/$', views.game_get_new_data, name='game_get_new_data'),
        url(r'^game/savescore/(?P<game_mode>[\w\-]+)/(?P<wpm>[-+]?[0-9]*\.?[0-9]+)/(?P<accuracy>[-+]?[0-9]*\.?[0-9]+)/$', views.game_add_new_score, name='game_add_new_score'),
        url(r'^game/savescore/(?P<game_mode>[\w\-]+)/(?P<wpm>[-+]?[0-9]*\.?[0-9]+)/(?P<accuracy>[-+]?[0-9]*\.?[0-9]+)/(?P<score>[\w\-]+)/$', views.game_add_new_score, name='game_add_new_score'),
        url(r'^game/$', views.game, name='game'),
        url(r'^statistics_personal/$', views.statistics_personal, name='statistics_personal'),
        url(r'^statistics_global/$', views.statistics_global, name='statistics_global'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^add_profile/$', views.register_profile, name='add_profile'),
        url(r'^friends_keydash/$', views.friends_keydash, name='friends_keydash'),
        url(r'^friends_requests_keydash/$', views.friends_requests_keydash, name='friends_requests_keydash'),
        url(r'^friendship_reject_keydash/(?P<friendship_request_id>[\w\-]+)/$', views.friendship_reject_keydash, name='friendship_reject_keydash'),
        url(r'^friendship_reject_accept/(?P<friendship_request_id>[\w\-]+)/$', views.friendship_accept_keydash, name='friendship_accept_keydash'),
        url(r'^suggest_friends/$', views.suggest_friends, name='suggest_friends')
        )