from rest_framework.permissions import BasePermission


class isOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner and obj.owner:
            return True
        else:
            return False
