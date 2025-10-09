
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from kanban_app.models import Board
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, TaskUpdateSerializer, CommentSerializer
from .permissions import IsBoardMemberOrOwner, IsTaskOwnerOrBoardMember, IsCommentAuthor
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class TaskCreateView(generics.CreateAPIView):

    """
    Create a new Task.

    Fields:
    - board: ID of the board
    - title: Task title
    - description: Task description
    - assignee_id: ID of the assigned user
    - reviewer_id: ID of the reviewer
    - due_date: Due date for the task

    The owner is automatically set to the currently authenticated user.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    def create(self, request, *args, **kwargs):
        board_id = request.data.get("board")
        if not board_id:
            return Response({"detail": "Board-ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return Response(
                {"error": "Board does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(owner=request.user)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Task by its ID.

    Permissions:
    - Only the task owner or the board owner can delete the task.
    - Other authenticated users may have read/write access depending on other permissions.

    Methods:
    - GET: Retrieve task details
    - PATCH: Partially update task
    - PUT: Fully update task (handled by DRF)
    - DELETE: Delete task (only owner or board owner)
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskOwnerOrBoardMember]

    def get_serializer_class(self):
        """
        Return appropriate serializer depending on request method.
        - GET: TaskSerializer (read-only)
        - PATCH/PUT: TaskUpdateSerializer
        """
        if self.request.method in ["GET"]:
            return TaskSerializer
        return TaskUpdateSerializer

    def patch(self, request, *args, **kwargs):
        """
        Partially update a task instance.
        """
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskUpdateSerializer(task).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Delete a task instance.
        Only allowed if the user is the task owner or the board owner.
        """
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignedTasksView(generics.ListAPIView):
    """
    List all tasks assigned to the logged-in user.

    Permissions:
    - User must be authenticated.

    GET /tasks/assigned-to-me/
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class ReviewingTasksView(generics.ListAPIView):
    """
    List all tasks where the logged-in user is the reviewer.

    Permissions:
    - User must be authenticated.

    GET /tasks/reviewing/
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class CommentListCreateView(generics.ListCreateAPIView):

    """
    List all comments for a specific task or create a new comment.

    Permissions:
    - User must be authenticated.
    - User must be a board member or board owner for the task.

    GET /tasks/<task_id>/comments/
        - List all comments for the task
    POST /tasks/<task_id>/comments/
        - Create a new comment for the task (author is automatically set to the logged-in user)
    """
    permission_classes = [IsAuthenticated, IsTaskOwnerOrBoardMember]
    serializer_class = CommentSerializer

    def get_queryset(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, task)
        return task.comments.all().order_by("created_at")

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, task)
        serializer.save(task=task, author=self.request.user)


class CommentDetailView(generics.RetrieveDestroyAPIView):

    """
    Retrieve or delete a specific comment for a task.

    Permissions:
    - Only the author of the comment can delete it.
    - User must be authenticated.

    Methods:
    - GET: Retrieve comment details
    - DELETE: Delete comment (only allowed for the author)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_object(self):
        """
        Retrieve the comment object based on task_pk and comment_pk from the URL.
        Checks object-level permissions.
        """
        task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
        comment = get_object_or_404(
            Comment, pk=self.kwargs['comment_pk'], task=task)
        self.check_object_permissions(self.request, comment)
        return comment

    def perform_destroy(self, instance):
        """
        Additional safety check in case IsCommentAuthor permission is bypassed.
        """
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()
