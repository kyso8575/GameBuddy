from django.urls import path
from .views import GameListView, GameDetailView

app_name = "games"
urlpatterns = [
    path('', GameListView.as_view(), name='games'),
    path('<int:game_id>/', GameDetailView.as_view(), name='game_detail'),
]
