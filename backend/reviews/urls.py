from django.urls import path
from . import views

urlpatterns = [
    # Basic review CRUD endpoints
    # GET /reviews/ (all reviews list, filter by query params)
    # POST /reviews/ (create new review - requires game_id in body)
    path('', views.ReviewListView.as_view(), name='review-list'),
    
    # Specific review detail endpoint
    # GET/PUT/DELETE /reviews/<review_id>/
    path('<int:review_id>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # Game-specific reviews API endpoint
    # GET /reviews/game/<game_id>/
    path('game/<int:game_id>/', views.GameReviewsView.as_view(), name='game-reviews'),
    
    # Current user's review for a specific game API endpoint
    # GET /reviews/game/<game_id>/user/
    path('game/<int:game_id>/user/', views.UserGameReviewView.as_view(), name='game-user-review'),
]
