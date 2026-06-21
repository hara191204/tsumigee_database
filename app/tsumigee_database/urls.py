from django.urls import path

from . import views

app_name = "tsumigee_database"

urlpatterns = [
    path("games/", views.GameListView.as_view(), name="game_list"),
    path("games/create/", views.GameCreateView.as_view(), name="game_create"),
    path("games/<int:pk>/", views.GameDetailView.as_view(), name="game_detail"),
    path("games/<int:pk>/update/", views.GameUpdateView.as_view(), name="game_update"),
    path("games/<int:pk>/delete/", views.GameDeleteView.as_view(), name="game_delete"),
]
