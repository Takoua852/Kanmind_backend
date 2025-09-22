from django.db import models
from django.conf import settings
from kanban_app.models import Board
from datetime import datetime


class Task(models.Model):

    STATUS_CHOICES = [
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    board = models.ForeignKey(
        Board, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium")
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reviewing_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="assigned_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    due_date = models.DateField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.title}(Board:{self.board.title})"

    @property
    def comments_count(self):
        # Zugriff über related_name="comments"
        return self.comments.count()


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
     return f"Comment by {self.author.fullname} on {self.task.title}"
