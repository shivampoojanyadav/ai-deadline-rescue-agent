from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_task, name="add_task"),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),
    path("delete/<int:pk>/", views.delete_task, name="delete_task"),
    path("complete/<int:pk>/", views.complete_task, name="complete_task"),
    path("analyze/<int:task_id>/", views.analyze_task_view, name="analyze_task"),
    path(
    "schedule/<int:task_id>/",
    views.schedule_task,
    name="schedule_task",
),

    path(
    "priority/<int:task_id>/",
    views.priority_task,
    name="priority_task",
),

    path(
    "recommend/<int:task_id>/",
    views.recommendation_task,
    name="recommendation_task",
),

    path(
    "goal/add/",
    views.add_goal,
    name="add_goal",
),

path(
    "habit/add/",
    views.add_habit,
    name="add_habit",
),

path(
    "habit/complete/<int:habit_id>/",
    views.complete_habit,
    name="complete_habit",
),

path(
    "voice/",
    views.voice_parser,
    name="voice"
),

path(
    "calendar/<int:task_id>/",
    views.export_calendar,
    name="export_calendar",
),

]