from django.contrib import admin
from keydash_app.models import UserProfile, Game, Score, MonthlyWeatherByCity

class GameAdmin(admin.ModelAdmin):
    list_display = ['game_mode']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'wpm', 'accuracy', 'score']

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['creator', 'friend']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'ranking_position', 'wpm_highest', 'accuracy_highest', 'score_highest']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(MonthlyWeatherByCity)