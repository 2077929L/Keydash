from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from keydash_app import views

class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/keydash/add_profile/'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^keydash/', include('keydash_app.urls')),
    url(r'^friendship/friend/requests/$', views.friends_keydash, name='friendship_view_friends'),
    url(r'^friendship/friends/(?P<username>[\w-]+)/$', views.friends_keydash, name='friendship_view_friends'),
    (r'^friendship/', include('friendship.urls')),
    # (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/change_password/$','django.contrib.auth.views.password_change',name="change_password"),
    url(r'^accounts/password_change/done/$','django.contrib.auth.views.password_change_done',name='password_change_done'),
    (r'^accounts/', include('registration.backends.simple.urls')),)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )

