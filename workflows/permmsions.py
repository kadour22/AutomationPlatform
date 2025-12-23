from rest_framework.permissions import BasePermission


def IsOwnerPermission(BasePermission) :
    def has_objects_permission(self, request, obj, view) :
        return request.user.role == "owner"

def ManagerPermission(BasePermission):
    def has_objects_permission(self, request, obj, view) :
        return request.user.role == "manager"