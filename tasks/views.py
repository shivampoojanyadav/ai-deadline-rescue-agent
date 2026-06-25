from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


def home(request):
    tasks = Task.objects.all().order_by("deadline")
    return render(request, "tasks/home.html", {"tasks": tasks})


def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = TaskForm()

    return render(request, "tasks/add_task.html", {"form": form})