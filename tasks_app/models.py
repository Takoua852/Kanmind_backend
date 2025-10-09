from django.db import models
from django.conf import settings
from kanban_app.models import Board
from datetime import datetime
from users_auth_app.models import User

class Task(models.Model):

    """
    Represents a task within a board.

    Fields:
    - board: The board to which this task belongs
    - title: Task title
    - description: Optional detailed description
    - owner: User who created the task
    - status: Task status (to-do, in-progress, review, done)
    - priority: Task priority (low, medium, high)
    - reviewer: User assigned as reviewer
    - assignee: User assigned to work on the task
    - due_date: Deadline for the task
    - updated_at: Last update timestamp
    """

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

    board = models.ForeignKey(Board, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, related_name="owned_tasks", on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviewing_tasks", null=True, blank=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="assigned_tasks",null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.title}(Board:{self.board.title})"

    @property
    def comments_count(self):
        return self.comments.count()

class Comment(models.Model):

    """
    Represents a task within a board.

    Fields:
    - board: The board to which this task belongs
    - title: Task title
    - description: Optional detailed description
    - owner: User who created the task
    - status: Task status (to-do, in-progress, review, done)
    - priority: Task priority (low, medium, high)
    - reviewer: User assigned as reviewer
    - assignee: User assigned to work on the task
    - due_date: Deadline for the task
    - updated_at: Last update timestamp
    """
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
     return f"Comment by {self.author.fullname} on {self.task.title}"
