from django import forms
from .models import Task, Goal, Habit


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "deadline",
            "priority",
            "estimated_hours",
        ]

        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["deadline"].input_formats = (
            "%Y-%m-%dT%H:%M",
        )

        self.fields["title"].widget.attrs.update({
            "id": "title",
            "class": "form-control"
        })

        self.fields["description"].widget.attrs.update({
            "id": "description",
            "class": "form-control"
        })

        self.fields["deadline"].widget.attrs.update({
            "id": "deadline",
            "class": "form-control"
        })

        self.fields["priority"].widget.attrs.update({
            "id": "priority",
            "class": "form-select"
        })

        self.fields["estimated_hours"].widget.attrs.update({
            "id": "estimated_hours",
            "class": "form-control"
        })

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = "__all__"


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = "__all__"