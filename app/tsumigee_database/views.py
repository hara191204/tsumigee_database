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
    paginate_by = 20

    def get_queryset(self):
        qs = Game.objects.select_related("maker", "hard")
        maker = self.request.GET.get("maker")
        hard = self.request.GET.get("hard")
        clear_statuses = self.request.GET.getlist("clear_status")
        grades = self.request.GET.getlist("grade")
        if maker:
            qs = qs.filter(maker_id=maker)
        if hard:
            qs = qs.filter(hard_id=hard)
        if clear_statuses:
            qs = qs.filter(clear_status__in=clear_statuses)
        if grades:
            qs = qs.filter(grade__in=grades)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["makers"] = Maker.objects.all()
        ctx["hards"] = Hard.objects.all()
        ctx["clear_status_choices"] = Game.ClearStatusChoices.choices
        ctx["grade_choices"] = Game.GradeChoices.choices
        ctx["filters"] = self.request.GET
        ctx["selected_clear_statuses"] = self.request.GET.getlist("clear_status")
        ctx["selected_grades"] = self.request.GET.getlist("grade")
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["filter_params"] = params.urlencode()
        return ctx


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
