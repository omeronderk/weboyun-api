from django.contrib import admin
from .models import Business, Game, BusinessGame, Reward, GamePlay


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'unique_code', 'network_ip_range']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(BusinessGame)
class BusinessGameAdmin(admin.ModelAdmin):
    list_display = ['business', 'game', 'win_probability']
    list_filter = ['business', 'game']


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['title', 'business_game']
    list_filter = ['business_game']


@admin.register(GamePlay)
class GamePlayAdmin(admin.ModelAdmin):
    list_display = ['business', 'game', 'ip_address', 'result', 'timestamp']
    list_filter = ['business', 'game']  # DÜZELTİLDİ

    def get_business(self, obj):
        return obj.business_game.business.name
    get_business.short_description = 'İşletme'

    def get_game(self, obj):
        return obj.business_game.game.name
    get_game.short_description = 'Oyun'
