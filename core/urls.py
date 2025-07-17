from django.urls import path
from .views import play_game
from . import views
from .views import GamePlayListView
urlpatterns = [
    path('api/play_game/', views.play_game, name='play_game'),
    path('api/business_games/<str:business_code>/', views.business_games, name='business_games'),
    path('api/gameplays/', GamePlayListView.as_view(), name='gameplay-list'),
]