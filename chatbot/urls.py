from django.urls import path
from . import views


app_name = "chatbot"
urlpatterns = [
    path("asdf/", views.asdf, name="asdf"),
]
