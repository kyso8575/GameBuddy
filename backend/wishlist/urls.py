from django.urls import path
from .views import WishlistListView, WishlistDetailView, WishlistStatusView

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistListView.as_view(), name='wishlist_list'),  # 위시리스트 목록 및 추가
    path('<int:game_id>/', WishlistDetailView.as_view(), name='wishlist_detail'),  # 위시리스트 개별 아이템 조회 및 삭제
    path('status/<int:game_id>/', WishlistStatusView.as_view(), name='wishlist_status'),  # 위시리스트 상태 확인
] 