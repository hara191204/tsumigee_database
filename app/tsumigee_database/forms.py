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
            "is_bishojo",
            "cleared_at",
            "note",
        ]
        widgets = {
            "cleared_at": forms.DateInput(attrs={"type": "date"}),
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

    def clean(self):
        cleaned_data = super().clean()
        clear_status = cleaned_data.get("clear_status")
        grade = cleaned_data.get("grade")
        if clear_status == Game.ClearStatusChoices.CLEAR:
            if grade == Game.GradeChoices.NA:
                self.add_error("grade", "クリア時は評価を設定してください。")
        else:
            if grade != Game.GradeChoices.NA:
                self.add_error("grade", "未クリア時は評価を「-」にしてください。")
        return cleaned_data


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
        fields = ["name", "furigana", "is_bishojo_brand"]


class HardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Hard
        fields = ["name"]
