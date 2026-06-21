from django import forms

from .models import Game, Hard, Maker


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "title",
            "furigana",
            "maker",
            "hard",
            "play_hard",
            "clear_status",
            "grade",
            "is_package",
            "is_bishoujo",
            "cleared_at",
            "note",
        ]
        widgets = {
            "cleared_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "note": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class MakerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Maker
        fields = ["name", "furigana", "is_bishoujo_brand"]


class HardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Hard
        fields = ["name"]
