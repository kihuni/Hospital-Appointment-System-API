from rest_framework import permissions
from .models import Role

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Role.objects.filter(user=request.user, role='PATIENT').exists()

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Role.objects.filter(user=request.user, role='DOCTOR').exists()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and Role.objects.filter(user=request.user, role='ADMIN').exists()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj.patient == request.user or 
            Role.objects.filter(user=request.user, role='ADMIN').exists()
        )