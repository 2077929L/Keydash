from django.contrib import admin
from keydash_app.models import UserProfile, Game, Score, Friendship

class GameAdmin(admin.ModelAdmin):
    list_display = ['game_mode']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'wpm', 'accuracy', 'score']

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['creator', 'friend']

admin.site.register(UserProfile)
admin.site.register(Game, GameAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Friendship, FriendshipAdmin)