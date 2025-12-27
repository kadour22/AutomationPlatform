from rest_framework.permissions import BasePermission

class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.role == "owner"
        )

def ManagerPermission(BasePermission):
    def has_object_permission(self, request, obj, view) :
        return request.user.role == "manager"
    
def IsAdmin(BasePermission):
    def has_object_permission(self, request, obj, view) :
        return request.user.role == "admin"
    
