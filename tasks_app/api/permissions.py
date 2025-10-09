from rest_framework.permissions import BasePermission
from kanban_app.models import Board
from rest_framework.exceptions import NotFound

class IsBoardMemberOrOwner(BasePermission):
    """
    Permission to allow access only if the user is the board owner or a member of the board.

    Applies to tasks:
    - The user must be the owner of the board the task belongs to, or a member.
    - Superusers always have access.
    """
    def has_permission(self, request, view):
         if request.method == "POST":
            board_id = request.data.get("board")
            if not board_id:
                raise NotFound("Board-ID is required.")
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                raise NotFound("Board does not exist.")

            user = request.user
            return (
                board.owner == user
                or board.members.filter(id=user.id).exists()
                or user.is_superuser
            )
         return True

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, "task"):
            obj = obj.task
        user = request.user
        return (obj.board.owner == user or
                obj.board.members.filter(id=user.id).exists() or
                user.is_superuser)


class IsTaskOwnerOrBoardMember(BasePermission):

    """
    Permission to allow DELETE only if the user is the task owner or a member of the board.

    Other HTTP methods (GET, PATCH, etc.) are allowed for all users who pass other permissions.
    Superusers can always delete.
    """

    def has_object_permission(self, request, view, obj):
 
        if hasattr(obj, "task"):
            obj = obj.task

        board = getattr(obj, "board", None)
        if not board:
            return False

        is_owner = board.owner == request.user
        is_member = board.members.filter(id=request.user.id).exists()
        is_superuser = request.user.is_superuser

        return is_owner or is_member or is_superuser

class IsCommentAuthor(BasePermission):
    """
    Permission to allow only the author of a comment to access or modify it.

    Example use cases:
    - DELETE: only the comment author can delete
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
