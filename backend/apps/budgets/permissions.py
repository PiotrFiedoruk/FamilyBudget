# permissions.py
from rest_framework import permissions


class IsOwnerOrShared(permissions.BasePermission):
    """
    Only budgets owned or shared with user
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.shared_with.all()
