from rest_framework.permissions import BasePermission
from tasks_app.models import Task

    
class IsBoardMemberOrOwner(BasePermission):
    """
    Erlaubt Zugriff nur, wenn der User Owner oder Mitglied des Boards der Task ist.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.board.owner == request.user or
                obj.board.members.filter(id=request.user.id).exists() or
                request.user.is_superuser)
    

class IsTaskOwnerOrBoardOwner(BasePermission):
    """
    Erlaubt DELETE nur, wenn der User Task-Ersteller oder Board-Owner ist.
    Für GET/PATCH reicht weiterhin IsBoardMemberOrOwner.
    """
    def has_object_permission(self, request, view, obj):
        # DELETE -> nur Ersteller oder Board-Owner
        if request.method == "DELETE":
            return (
                obj.created_by == request.user
                or obj.board.owner == request.user
            )
        return True
    
class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
