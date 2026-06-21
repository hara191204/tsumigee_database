from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import GameForm
from .models import Game


class GameListView(ListView):
    model = Game
    template_name = "tsumigee_database/game_list.html"


class GameDetailView(DetailView):
    model = Game
    template_name = "tsumigee_database/game_detail.html"


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = "tsumigee_database/game_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "追加"
        return ctx


class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm
    template_name = "tsumigee_database/game_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "編集"
        return ctx


class GameDeleteView(DeleteView):
    model = Game
    template_name = "tsumigee_database/game_confirm_delete.html"
    success_url = reverse_lazy("tsumigee_database:game_list")
