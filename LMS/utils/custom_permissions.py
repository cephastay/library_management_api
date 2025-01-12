from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow object owners to have write access, 
    while granting read-only access for safe methods 
    (e.g., GET, HEAD, OPTIONS).
    """
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        """
        Allow access if the request method is safe or the user is authenticated.
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated  

    def has_object_permission(self, request, view, obj):
        """
        Allow read-only access for safe methods or ensure 
        the user owns the object.
        """
        if request.method in SAFE_METHODS:
            return True  
        return obj == request.user


class IsUser(BasePermission):
    """
    Permission to ensure the user is authenticated and is 
    accessing their own object.
    """

    def has_permission(self, request, view):
        """
        Allow access if the user is authenticated.
        """
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Allow access only if the user owns the object.
        """
        return obj == request.user


class IsOwnerOrAdmin(BasePermission):
    """
    Permission to allow object owners or staff/admin users 
    to access the object.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow access for admin users or if the user owns the object.
        """
        if request.user.is_staff:
            return True
        return obj == request.user


class HasAccountOrNone(BasePermission):
    """
    Permission to deny access if the user already has an account 
    unless they are staff.
    """
    message = 'Access denied: You already have an account, or you must be a staff user.'

    def has_permission(self, request, view):
        """
        Allow access for staff users or unauthenticated users.
        Deny access for authenticated users with an account.
        """
        if request.user.is_staff:
            return True
        elif request.user and request.user.is_authenticated:
            return False
        return True
