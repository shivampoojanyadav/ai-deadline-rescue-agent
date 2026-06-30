from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone

from django.http import HttpResponse
from datetime import timedelta

from .models import Task, Goal, Habit
from .forms import TaskForm, GoalForm, HabitForm
from .ai import (
    analyze_task,
    generate_schedule,
    recommend_priority,
    productivity_recommendation,
    parse_voice_command,
)

def home(request):
    
    search = request.GET.get("search")

    priority = request.GET.get("priority")
    status = request.GET.get("status")

    tasks = Task.objects.all()

    if search:
        tasks = tasks.filter(title__icontains=search)

    if priority:
        tasks = tasks.filter(priority=priority)

    if status == "completed":
        tasks = tasks.filter(completed=True)

    elif status == "pending":
        tasks = tasks.filter(completed=False)

    tasks = tasks.order_by("deadline")


    now = timezone.now()

    for task in tasks:
        task.days_left = (task.deadline - now).days

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = Task.objects.filter(completed=False).count()
    

    overdue_count = Task.objects.filter(
        completed=False,
        deadline__lt=timezone.now()
    ).count()

    completion_rate = 0

    if total_tasks > 0:
        completion_rate = round(
        (completed_tasks / total_tasks) * 100
    )

    # Goal Statistics
    goals = Goal.objects.all()

    total_goals = Goal.objects.count()

    completed_goals = Goal.objects.filter(completed=True).count()

    if total_goals > 0:
        goal_progress = int((completed_goals / total_goals) * 100)
    else:
        goal_progress = 0


    habits = Habit.objects.all()

    completed_habits = Habit.objects.filter(completed_today=True).count()

    total_habits = Habit.objects.count()

    if total_habits > 0:
        habit_progress = int((completed_habits / total_habits) * 100)
    else:
        habit_progress = 0


    today = timezone.now().date()

    due_today = Task.objects.filter(
        completed=False,
    deadline__date=today
        ).count()

    overdue_tasks = Task.objects.filter(
    completed=False,
    deadline__lt=timezone.now()
).count()

    upcoming_tasks = Task.objects.filter(
    completed=False,
    deadline__date__gt=today
    ).count()
    high_tasks = Task.objects.filter(priority="High").count()
    medium_tasks = Task.objects.filter(priority="Medium").count()
    low_tasks = Task.objects.filter(priority="Low").count()
    return render(request, "tasks/home.html", {
    "tasks": tasks,
    "total_tasks": total_tasks,
    "completed_tasks": completed_tasks,
    "pending_tasks": pending_tasks,
    "search": search,
    "priority": priority,
    "status": status,
    "high_tasks": high_tasks,
    "medium_tasks": medium_tasks,
    "low_tasks": low_tasks,
    "due_today": due_today,
    "overdue_tasks": overdue_tasks,
    "upcoming_tasks": upcoming_tasks,
    "goals": goals,
    "goal_progress": goal_progress,
    "completed_goals": completed_goals,
    "total_goals": total_goals,
    "habits": habits,
    "completed_habits": completed_habits,
    "total_habits": total_habits,
    "habit_progress": habit_progress,
    "completion_rate": completion_rate,
    "overdue_count": overdue_count,
})


def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = TaskForm()

    return render(request, "tasks/add_task.html", {"form": form})


def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/add_task.html", {"form": form})


def delete_task(request, pk):

    task = Task.objects.get(id=pk)
    task.delete()

    return redirect("home")

def complete_task(request, pk):

    task = Task.objects.get(id=pk)

    task.completed = True
    task.save()

    return redirect("home")

def analyze_task_view(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    result = analyze_task(
        task.title,
        task.description,
        task.deadline,
        task.priority,
        task.estimated_hours,
    )

    task.ai_analysis = result
    task.save()

    return redirect("home")


   

def schedule_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    schedule = generate_schedule(
        task.title,
        task.description,
        task.deadline,
        task.priority,
        task.estimated_hours,
    )

    task.ai_schedule = schedule
    task.save()

    return redirect("home")



def priority_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    result = recommend_priority(
        task.title,
        task.description,
        task.deadline,
        task.priority,
        task.estimated_hours,
    )

    task.ai_priority = result
    task.save()

    return redirect("home")


def recommendation_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    result = productivity_recommendation(
        task.title,
        task.description,
        task.deadline,
        task.estimated_hours,
    )

    task.ai_recommendation = result
    task.save()

    return redirect("home")


def add_goal(request):

    form = GoalForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("home")

    return render(request, "tasks/add_goal.html", {
        "form": form
    })

def add_habit(request):

    form = HabitForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("home")

    return render(request, "tasks/add_habit.html", {
        "form": form
    })


def complete_habit(request, habit_id):

    habit = Habit.objects.get(id=habit_id)

    habit.completed_today = True
    habit.streak += 1

    habit.save()

    return redirect("home")


from django.http import JsonResponse
import json

def voice_parser(request):

    if request.method == "POST":

        body = json.loads(request.body)

        result = parse_voice_command(
            body["command"]
        )

        return JsonResponse(result)
    

from django.http import JsonResponse
import json

def voice_parser(request):

    if request.method == "POST":

        body = json.loads(request.body)

        result = parse_voice_command(body["command"])

        return JsonResponse(result)
    

def export_calendar(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    start = task.deadline
    end = start + timedelta(hours=task.estimated_hours)

    content = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{task.title}
DESCRIPTION:{task.description}
DTSTART:{start.strftime('%Y%m%dT%H%M%S')}
DTEND:{end.strftime('%Y%m%dT%H%M%S')}
END:VEVENT
END:VCALENDAR
"""

    response = HttpResponse(content, content_type="text/calendar")

    response["Content-Disposition"] = f'attachment; filename="{task.title}.ics"'

    return response