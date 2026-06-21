from django.db.models import Count, Q
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

_VALID_SORT_FIELDS = {
    "furigana",
    "maker__furigana",
    "hard__name",
    "clear_status",
    "grade",
    "is_package",
    "is_bishoujo",
    "created_at",
    "cleared_at",
    "note",
}


class GameListView(ListView):
    model = Game
    template_name = "tsumigee_database/game_list.html"
    paginate_by = 20

    def _get_sort(self):
        sort = self.request.GET.get("sort", "furigana")
        if sort.lstrip("-") not in _VALID_SORT_FIELDS:
            return "furigana"
        return sort

    def _get_filtered_qs(self):
        qs = Game.objects.select_related("maker", "hard", "play_hard")
        maker = self.request.GET.get("maker")
        hard = self.request.GET.get("hard")
        clear_statuses = self.request.GET.getlist("clear_status")
        grades = self.request.GET.getlist("grade")
        is_package = self.request.GET.get("is_package", "")
        is_bishoujo = self.request.GET.get("is_bishoujo", "")
        if maker:
            qs = qs.filter(maker_id=maker)
        if hard:
            qs = qs.filter(hard_id=hard)
        if clear_statuses:
            qs = qs.filter(clear_status__in=clear_statuses)
        if grades:
            qs = qs.filter(grade__in=grades)
        if is_package != "":
            qs = qs.filter(is_package=is_package == "true")
        if is_bishoujo != "":
            qs = qs.filter(is_bishoujo=is_bishoujo == "true")
        return qs

    def get_queryset(self):
        return self._get_filtered_qs().order_by(self._get_sort())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["makers"] = Maker.objects.all()
        ctx["hards"] = Hard.objects.all()
        ctx["clear_status_choices"] = Game.ClearStatusChoices.choices
        ctx["grade_choices"] = Game.GradeChoices.choices
        ctx["selected_maker"] = self.request.GET.get("maker", "")
        ctx["selected_hard"] = self.request.GET.get("hard", "")
        ctx["selected_clear_statuses"] = self.request.GET.getlist("clear_status")
        ctx["selected_grades"] = self.request.GET.getlist("grade")
        ctx["selected_is_package"] = self.request.GET.get("is_package", "")
        ctx["selected_is_bishoujo"] = self.request.GET.get("is_bishoujo", "")
        sort = self._get_sort()
        ctx["sort_field"] = sort.lstrip("-")
        ctx["sort_order"] = "desc" if sort.startswith("-") else "asc"
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["filter_params"] = params.urlencode()
        base_params = self.request.GET.copy()
        base_params.pop("page", None)
        base_params.pop("sort", None)
        ctx["base_params"] = base_params.urlencode()
        agg = self._get_filtered_qs().aggregate(
            total=Count("id"),
            clear=Count("id", filter=Q(clear_status=Game.ClearStatusChoices.CLEAR)),
            tsumi=Count("id", filter=Q(clear_status=Game.ClearStatusChoices.TSUMI)),
            na=Count("id", filter=Q(clear_status=Game.ClearStatusChoices.NA)),
        )
        total = agg["total"]
        ctx["stats"] = {
            **agg,
            "tsumi_ratio": round(agg["tsumi"] / total * 100, 1) if total else 0,
        }
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


class MakerDetailView(DetailView):
    model = Maker
    template_name = "tsumigee_database/maker_detail.html"


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


class HardDetailView(DetailView):
    model = Hard
    template_name = "tsumigee_database/hard_detail.html"


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
