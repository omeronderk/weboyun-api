from django.urls import path
from .views import play_game
from . import views
urlpatterns = [
    path('api/play_game/', views.play_game, name='play_game'),
    path('api/business_games/<str:business_code>/', views.business_games, name='business_games'),
]