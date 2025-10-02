from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    """
    Permission to allow access only if the user is the board owner or a member of the board.

    Applies to tasks:
    - The user must be the owner of the board the task belongs to, or a member.
    - Superusers always have access.
    """

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, "task"):
            obj = obj.task

        return (obj.board.owner == request.user or
                obj.board.members.filter(id=request.user.id).exists() or
                request.user.is_superuser)


class IsTaskOwnerOrBoardMember(BasePermission):

    """
    Permission to allow DELETE only if the user is the task owner or a member of the board.

    Other HTTP methods (GET, PATCH, etc.) are allowed for all users who pass other permissions.
    Superusers can always delete.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "task"):
            obj = obj.task
        if request.method == "DELETE":
            return (
                obj.owner == request.user or
                obj.board.members.filter(
                    id=request.user.id).exists() or request.user.is_superuser
            )
        return True


class IsCommentAuthor(BasePermission):
    """
    Permission to allow only the author of a comment to access or modify it.

    Example use cases:
    - DELETE: only the comment author can delete
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
