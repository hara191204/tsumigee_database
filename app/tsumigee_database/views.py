from django.views.generic import ListView

from .models import Game


class GameListView(ListView):
    model = Game
    template_name = "tsumigee_database/game_list.html"
