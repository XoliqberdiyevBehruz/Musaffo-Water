from django.http import Http404

from rest_framework.permissions import BasePermission

class IsStaffOr404(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return Http404