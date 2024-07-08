from rest_framework.permissions import BasePermission

class IsBuyerOrSeller(BasePermission):
    """
    Allows access only to users with the 'buyer' or 'seller' role.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.role == 'buyer' or request.user.role == 'seller')
