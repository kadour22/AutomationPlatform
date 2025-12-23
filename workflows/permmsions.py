from rest_framework.permissions import BasePermission


def IsOwnerPermission(BasePermission) :
    def has_objects_permission(self, request, obj, view) :
        return request.user.role == "owner"

def ManagerPermission(BasePermission):
    def has_objects_permission(self, request, obj, view) :
        return request.user.role == "manager"
    

def IsAdmin(BasePermission):
    def has_objects_permission(self, request, obj, view) :
        return request.user.role == "admin"
    

def IsEmployee(BasePermission):
    def has_objects_permission(self, request, obj, view) :
        return request.user.role == "employee"
    
# IsAdmin , IsEmployee