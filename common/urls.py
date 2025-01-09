from django.urls import path
from . import views

app_name = "common"
urlpatterns = [
    path('home/', views.home, name='home'),
    #path('search/', views.SearchFormView.as_view(), name='search'),
]