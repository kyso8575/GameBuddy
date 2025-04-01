from django.urls import path
from . import views



app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
    path('profile/<int:id>/', views.UserProfileAPIView.as_view(), name='profile'),
    path('current-user/', views.CurrentUserView.as_view(), name='current_user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
