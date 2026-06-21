from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import GameForm, HardForm, MakerForm
from .models import Game, Hard, Maker


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


# --- Maker ---


class MakerListView(ListView):
    model = Maker
    template_name = "tsumigee_database/maker_list.html"


class MakerCreateView(CreateView):
    model = Maker
    form_class = MakerForm
    template_name = "tsumigee_database/maker_form.html"
    success_url = reverse_lazy("tsumigee_database:maker_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "追加"
        return ctx


class MakerUpdateView(UpdateView):
    model = Maker
    form_class = MakerForm
    template_name = "tsumigee_database/maker_form.html"
    success_url = reverse_lazy("tsumigee_database:maker_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "編集"
        return ctx


class MakerDeleteView(DeleteView):
    model = Maker
    template_name = "tsumigee_database/maker_confirm_delete.html"
    success_url = reverse_lazy("tsumigee_database:maker_list")


# --- Hard ---


class HardListView(ListView):
    model = Hard
    template_name = "tsumigee_database/hard_list.html"


class HardCreateView(CreateView):
    model = Hard
    form_class = HardForm
    template_name = "tsumigee_database/hard_form.html"
    success_url = reverse_lazy("tsumigee_database:hard_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "追加"
        return ctx


class HardUpdateView(UpdateView):
    model = Hard
    form_class = HardForm
    template_name = "tsumigee_database/hard_form.html"
    success_url = reverse_lazy("tsumigee_database:hard_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action"] = "編集"
        return ctx


class HardDeleteView(DeleteView):
    model = Hard
    template_name = "tsumigee_database/hard_confirm_delete.html"
    success_url = reverse_lazy("tsumigee_database:hard_list")
