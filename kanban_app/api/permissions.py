from rest_framework import permissions
from rest_framework.permissions import BasePermission

     
class IsBoardMemberOrOwner(permissions.BasePermission):
    """
    Zugriff nur für Owner oder Mitglieder des Boards.
    """

    def has_object_permission(self, request, view, obj):
        # Zugriff erlaubt, wenn User = Owner
        if obj.owner == request.user:
            return True

        # Zugriff erlaubt, wenn User Mitglied des Boards ist
        if request.user in obj.members.all():
            return True
        
        if request.user.is_superuser:
            return True

        return False
    

class IsBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user