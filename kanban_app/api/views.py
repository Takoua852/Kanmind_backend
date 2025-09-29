
from rest_framework import generics
from kanban_app.api.serializers import BoardSerializer, BoardCreateSerializer,BoardDetailSerializer, BoardUpdateSerializer
from kanban_app.models import Board
from .permissions import  IsBoardMemberOrOwner,IsBoardOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from users_auth_app.models import User

class BoardListView(generics.ListCreateAPIView):
    permission_classes = [ IsAuthenticated,IsBoardMemberOrOwner]

    def get_queryset(self):
        user = self.request.user
        return [
            board for board in Board.objects.all()
            if board.owner == user or user in board.members.all() or user.is_superuser
        ]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BoardCreateSerializer
        return BoardSerializer

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner| IsBoardOwner]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BoardUpdateSerializer
        return BoardDetailSerializer
    
    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Nur der Owner kann das Board löschen.")
        instance.delete()

