from rest_framework import permissions


class IsManager(permissions.BasePermission):
    message = "User is not a manager"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsDeliveryCrew(permissions.BasePermission):
    message = "User is not a delivery crew member"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery Crew').exists()

class IsCustomer(permissions.BasePermission):
    message = "User is not a Customer"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Customer').exists()
