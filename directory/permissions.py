from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow superadmins to access.
    """
    def has_permission(self, request, view):
        return (request.user and 
                hasattr(request.user, 'permission') and 
                request.user.permission == 'superadmin')

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Custom permission to allow both admins and superadmins to access.
    """
    def has_permission(self, request, view):
        return (request.user and 
                hasattr(request.user, 'permission') and 
                request.user.permission in ['admin', 'superadmin'])

class IsSuperAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Superadmins: full access (read, write, delete)
    - Admins: read-only access
    """
    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, 'permission'):
            return False
        
        # Allow all access for superadmins
        if request.user.permission == 'superadmin':
            return True
        
        # Allow only read access for admins
        if request.user.permission == 'admin':
            return request.method in permissions.SAFE_METHODS
        
        return False
    
class CanManageAdmins(permissions.BasePermission):
    """
    Only superadmins can manage admin accounts
    """
    def has_permission(self, request, view):
        return True