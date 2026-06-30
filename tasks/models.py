from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    deadline = models.DateTimeField()

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
    )

    estimated_hours = models.PositiveIntegerField(default=1)

    ai_analysis = models.TextField(blank=True)

    ai_schedule = models.TextField(blank=True)

    ai_priority = models.TextField(blank=True)

    ai_recommendation = models.TextField(blank=True)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class Goal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Habit(models.Model):
    name = models.CharField(max_length=200)
    streak = models.IntegerField(default=0)
    completed_today = models.BooleanField(default=False)

    def __str__(self):
        return self.name