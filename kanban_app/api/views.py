
from rest_framework import generics, status
from kanban_app.api.serializers import BoardSerializer, BoardCreateSerializer, BoardDetailSerializer, BoardUpdateSerializer, EmailCheckSerializer
from kanban_app.models import Board
from .permissions import IsBoardMemberOrOwner, IsBoardOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from users_auth_app.models import User


class BoardListView(generics.ListCreateAPIView):

    """
    GET: List all boards accessible by the current user.
    POST: Create a new board. The logged-in user becomes the owner.
    """
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]

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

    """
    GET: Retrieve board details.
    PUT/PATCH: Update board information.
    DELETE: Delete the board (owner only).
    """
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner | IsBoardOwner]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BoardUpdateSerializer
        return BoardDetailSerializer

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("only the owner can delete the board.")
        instance.delete()


class EmailCheckView(generics.GenericAPIView):

    """
    GET: Check if a user with the given email exists.
    """
    serializer_class = EmailCheckSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")

        if not email:
            return Response({"detail": "E-Mail doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"detail": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
