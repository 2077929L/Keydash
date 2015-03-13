from django.conf.urls import patterns, url
from keydash_app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='front'),
        url(r'^home', views.index, name='home'),
        url(r'^about', views.about, name='about'),
        url(r'^trial', views.trial, name='trial'),
        url(r'^game', views.game, name='game'),
        url(r'^statistics', views.statistics, name='statistics'),
        url(r'^profile', views.profile, name='profile'),
        )