from django.urls import path
# from .views import ReviewingTasksView, AssignedTasksView, TaskCreateView
from .views import TaskCreateView, TaskDetailView, ReviewingTasksView, AssignedTasksView, CommentListCreateView, CommentDetailView

urlpatterns = [
    path('tasks/assigned-to-me/', AssignedTasksView.as_view(), name="assigned-tasks"),
    path('tasks/reviewing/', ReviewingTasksView.as_view(), name="task-review"),
    path('tasks/', TaskCreateView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path('tasks/<int:pk>/comments/',
         CommentListCreateView.as_view(), name='task-comments'),
    path('tasks/<int:task_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view(), name='comment-detail')]
