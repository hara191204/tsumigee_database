from django.urls import path

from . import views

app_name = "tsumigee_database"

urlpatterns = [
    path("games/", views.GameListView.as_view(), name="game_list"),
]
