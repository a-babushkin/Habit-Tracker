from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли текущий пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


#
# class IsAdmin(permissions.BasePermission):
#     """Проверяет, является ли текущий пользователь администратором"""
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_staff:
#             return True
#         return False
