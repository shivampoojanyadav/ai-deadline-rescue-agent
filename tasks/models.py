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

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title