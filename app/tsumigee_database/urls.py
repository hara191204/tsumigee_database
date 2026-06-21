from django.urls import path

from . import views

app_name = "tsumigee_database"

urlpatterns = [
    # Game
    path("games/", views.GameListView.as_view(), name="game_list"),
    path("games/create/", views.GameCreateView.as_view(), name="game_create"),
    path("games/<int:pk>/", views.GameDetailView.as_view(), name="game_detail"),
    path("games/<int:pk>/update/", views.GameUpdateView.as_view(), name="game_update"),
    path("games/<int:pk>/delete/", views.GameDeleteView.as_view(), name="game_delete"),
    # Maker
    path("makers/", views.MakerListView.as_view(), name="maker_list"),
    path("makers/create/", views.MakerCreateView.as_view(), name="maker_create"),
    path(
        "makers/<int:pk>/update/", views.MakerUpdateView.as_view(), name="maker_update"
    ),
    path(
        "makers/<int:pk>/delete/", views.MakerDeleteView.as_view(), name="maker_delete"
    ),
    # Hard
    path("hards/", views.HardListView.as_view(), name="hard_list"),
    path("hards/create/", views.HardCreateView.as_view(), name="hard_create"),
    path("hards/<int:pk>/update/", views.HardUpdateView.as_view(), name="hard_update"),
    path("hards/<int:pk>/delete/", views.HardDeleteView.as_view(), name="hard_delete"),
]
