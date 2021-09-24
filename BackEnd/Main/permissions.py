from rest_framework import permissions


class BankPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.profile.Type == request.user.profile.PERSONNEL:
            return True
        return False


class ProviderPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.profile.Type == request.user.profile.PROVIDERS:
            return True
        return False


class CustomerPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.profile.Type == request.user.profile.CUSTOMERS:
            return True
        return False
