
from rest_framework import generics, status
from kanban_app.api.serializers import BoardSerializer, BoardCreateSerializer, BoardDetailSerializer, BoardUpdateSerializer, EmailCheckSerializer
from kanban_app.models import Board
from .permissions import IsBoardMemberOrOwner, IsBoardOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from users_auth_app.models import User
from drf_spectacular.utils import extend_schema


@extend_schema(
    request=BoardCreateSerializer,
    responses=BoardSerializer,
    description=(
        "List all boards the current user has access to or create a new board. "
        "User must be the owner, a member, or a superuser."
    )
)

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

@extend_schema(
    request=BoardUpdateSerializer,
    responses=BoardDetailSerializer,
    description=(
        "Retrieve, update, or delete a board. "
        "Only the board owner can delete the board."
    )
)
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
            raise PermissionDenied("Nur der Owner kann das Board löschen.")
        instance.delete()

@extend_schema(
    responses=EmailCheckSerializer,
    description=(
        "Check if a user exists by email. "
        "Returns 200 with user data if found, 404 if not found."
    )
)
class EmailCheckView(generics.GenericAPIView):
    
    """
    GET: Check if a user with the given email exists.
    """
    serializer_class = EmailCheckSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")

        if not email:
            return Response({"detail": "E-Mail-Parameter fehlt"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Email nicht gefunden"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"detail": "Interner Serverfehler"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
