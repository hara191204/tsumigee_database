from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse, reverse_lazy
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
    "is_bishojo",
    "created_at",
    "cleared_at",
    "note",
}


class ActionMixin(LoginRequiredMixin):
    action = ""

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"action": self.action}


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = "tsumigee_database/game_list.html"
    paginate_by = 500

    def get(self, request, *args, **kwargs):
        request.session["game_list_params"] = request.GET.urlencode()
        return super().get(request, *args, **kwargs)

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
        is_bishojo = self.request.GET.get("is_bishojo", "")
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
        if is_bishojo != "":
            qs = qs.filter(is_bishojo=is_bishojo == "true")
        return qs

    def _get_page_range(self, page_obj):
        current = page_obj.number
        total = page_obj.paginator.num_pages
        delta = 2
        edges = {1, 2, total - 1, total}
        window = set(range(max(1, current - delta), min(total, current + delta) + 1))
        pages = sorted(p for p in (edges | window) if 1 <= p <= total)
        result = []
        prev = None
        for p in pages:
            if prev is not None and p - prev > 1:
                result.append(None)
            result.append(p)
            prev = p
        return result

    def get_queryset(self):
        sort = self._get_sort()
        order = [sort]
        if sort.lstrip("-") != "furigana":
            order.append("furigana")
        return self._get_filtered_qs().order_by(*order)

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
        ctx["selected_is_bishojo"] = self.request.GET.get("is_bishojo", "")
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
        ctx["filter_count"] = sum(
            [
                1 if self.request.GET.get("maker") else 0,
                1 if self.request.GET.get("hard") else 0,
                len(self.request.GET.getlist("clear_status")),
                len(self.request.GET.getlist("grade")),
                1 if self.request.GET.get("is_package") else 0,
                1 if self.request.GET.get("is_bishojo") else 0,
            ]
        )
        if ctx.get("is_paginated"):
            ctx["page_range"] = self._get_page_range(ctx["page_obj"])
        agg = self._get_filtered_qs().aggregate(
            total=Count("id"),
            clear=Count("id", filter=Q(clear_status=Game.ClearStatusChoices.CLEAR)),
            tsumi=Count("id", filter=Q(clear_status=Game.ClearStatusChoices.TSUMI)),
            collection_only=Count(
                "id", filter=Q(clear_status=Game.ClearStatusChoices.COLLECTION_ONLY)
            ),
        )
        playable = agg["clear"] + agg["tsumi"]
        ctx["stats"] = {
            **agg,
            "tsumi_ratio": round(agg["tsumi"] / playable * 100, 1) if playable else 0,
        }
        return ctx


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = "tsumigee_database/game_detail.html"


class GameCreateView(ActionMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = "tsumigee_database/game_form.html"
    action = "追加"


class GameUpdateView(ActionMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = "tsumigee_database/game_form.html"
    action = "編集"

    def get_success_url(self):
        params = self.request.session.get("game_list_params", "")
        url = reverse("tsumigee_database:game_list")
        return f"{url}?{params}" if params else url


class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game

    def get_success_url(self):
        params = self.request.session.get("game_list_params", "")
        url = reverse("tsumigee_database:game_list")
        return f"{url}?{params}" if params else url


# --- Maker ---


class MakerDetailView(LoginRequiredMixin, DetailView):
    model = Maker
    template_name = "tsumigee_database/maker_detail.html"


_MAKER_VALID_SORT_FIELDS = {"name", "furigana", "is_bishojo_brand", "created_at"}


class MakerListView(LoginRequiredMixin, ListView):
    model = Maker
    template_name = "tsumigee_database/maker_list.html"

    def _get_sort(self):
        sort = self.request.GET.get("sort", "furigana")
        if sort.lstrip("-") not in _MAKER_VALID_SORT_FIELDS:
            return "furigana"
        return sort

    def get_queryset(self):
        sort = self._get_sort()
        order = [sort]
        if sort.lstrip("-") != "furigana":
            order.append("furigana")
        return Maker.objects.order_by(*order)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        sort = self._get_sort()
        ctx["sort_field"] = sort.lstrip("-")
        ctx["sort_order"] = "desc" if sort.startswith("-") else "asc"
        ctx["base_params"] = ""
        return ctx


class MakerCreateView(ActionMixin, CreateView):
    model = Maker
    form_class = MakerForm
    template_name = "tsumigee_database/maker_form.html"
    success_url = reverse_lazy("tsumigee_database:maker_list")
    action = "追加"


class MakerUpdateView(ActionMixin, UpdateView):
    model = Maker
    form_class = MakerForm
    template_name = "tsumigee_database/maker_form.html"
    success_url = reverse_lazy("tsumigee_database:maker_list")
    action = "編集"


class MakerDeleteView(LoginRequiredMixin, DeleteView):
    model = Maker
    success_url = reverse_lazy("tsumigee_database:maker_list")


# --- Hard ---


class HardDetailView(LoginRequiredMixin, DetailView):
    model = Hard
    template_name = "tsumigee_database/hard_detail.html"


class HardListView(LoginRequiredMixin, ListView):
    model = Hard
    template_name = "tsumigee_database/hard_list.html"


class HardCreateView(ActionMixin, CreateView):
    model = Hard
    form_class = HardForm
    template_name = "tsumigee_database/hard_form.html"
    success_url = reverse_lazy("tsumigee_database:hard_list")
    action = "追加"


class HardUpdateView(ActionMixin, UpdateView):
    model = Hard
    form_class = HardForm
    template_name = "tsumigee_database/hard_form.html"
    success_url = reverse_lazy("tsumigee_database:hard_list")
    action = "編集"


class HardDeleteView(LoginRequiredMixin, DeleteView):
    model = Hard
    success_url = reverse_lazy("tsumigee_database:hard_list")
