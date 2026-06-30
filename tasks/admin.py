from django.contrib import admin
from .models import Task, Goal, Habit


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "priority",
        "deadline",
        "completed",
        "created_at",
    )

    list_filter = (
        "priority",
        "completed",
    )

    search_fields = (
        "title",
        "description",
    )

admin.site.register(Goal)

admin.site.register(Habit)