from rest_framework import permissions

class IsBookingOwnerOrFieldOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.field.owner == request.user