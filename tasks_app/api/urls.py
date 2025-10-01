from django.urls import path
from .views import TaskCreateView, TaskDetailView, ReviewingTasksView, AssignedTasksView, CommentListCreateView, CommentDetailView


"""
Task and Comment API Endpoints.

Tasks:
1. /tasks/assigned-to-me/     - GET: List tasks assigned to the logged-in user
2. /tasks/reviewing/          - GET: List tasks where the user is the reviewer
3. /tasks/                    - GET: List all tasks, POST: Create a new task
4. /tasks/<pk>/               - GET: Retrieve a task, PATCH/PUT: Update, DELETE: Delete task

Comments:
5. /tasks/<pk>/comments/      - GET: List comments for a task, POST: Create comment
6. /tasks/<task_pk>/comments/<comment_pk>/ - GET: Retrieve comment, DELETE: Delete comment
"""
urlpatterns = [
    path('tasks/assigned-to-me/', AssignedTasksView.as_view(), name="assigned-tasks"),
    path('tasks/reviewing/', ReviewingTasksView.as_view(), name="task-review"),
    path('tasks/', TaskCreateView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path('tasks/<int:pk>/comments/', CommentListCreateView.as_view(), name='task-comments'),
    path('tasks/<int:task_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view(), name='comment-detail')]
