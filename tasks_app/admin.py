from django.contrib import admin
from .models import Task, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "board", "board_id","assignee", "reviewer", "status", "priority", "due_date", "comments_count")
    list_filter = ("status", "priority", "due_date", "board")
    search_fields = ("title", "description", "assignee__email", "reviewer__email")
    raw_id_fields = ("assignee", "reviewer")  

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "author", "created_at", "short_content")
    search_fields = ("content", "author__email", "task__title")
    list_filter = ("created_at",)

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"
