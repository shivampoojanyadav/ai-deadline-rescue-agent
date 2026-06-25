from django import forms
from .models import Task


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