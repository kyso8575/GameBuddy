from django.urls import path
from .views import WishlistView, WishlistGameView

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist'),  # 위시리스트 목록 조회, 추가, 삭제
    path('game/<int:game_id>/', WishlistGameView.as_view(), name='wishlist_game'),  # 특정 게임의 위시리스트 상태 확인 및 삭제
] 