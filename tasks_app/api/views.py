
from rest_framework import generics, status

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, TaskUpdateSerializer, CommentSerializer, CommentCreateSerializer
from .permissions import IsBoardMemberOrOwner, IsTaskOwnerOrBoardOwner, IsCommentAuthor
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated,
                          IsBoardMemberOrOwner, IsTaskOwnerOrBoardOwner]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return TaskSerializer
        return TaskUpdateSerializer

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskUpdateSerializer(task).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignedTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class ReviewingTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

    def get_queryset(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        return task.comments.all().order_by("created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        serializer.save(task=task, author=self.request.user)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = CommentSerializer

    def get_object(self):
     task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
     comment = get_object_or_404(
        Comment, pk=self.kwargs['comment_pk'], task=task)
     self.check_object_permissions(self.request, comment)
     return comment

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                "Du darfst nur deine eigenen Kommentare löschen.")
        instance.delete()
