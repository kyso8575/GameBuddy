from django.urls import path
from . import views


app_name = "chatbot"
urlpatterns = [
    path("process_session/", views.ProcessSessionView.as_view(), name="process_session"),
    path("load_session/", views.LoadSessionView.as_view(), name="load_session"),
    path("start_session/", views.StartSessionView.as_view(), name="start_session"),
]
