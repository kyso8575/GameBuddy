from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path("signup/", views.signup, name='signup'),
    path("signup_complete/", views.signup_complete, name='signup_complete'),
    path('check-username/', views.check_username, name='check_username'),
    path('check-nickname/', views.check_nickname, name='check_nickname'),
]