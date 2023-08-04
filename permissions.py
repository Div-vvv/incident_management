from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'User required to perform this action'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user