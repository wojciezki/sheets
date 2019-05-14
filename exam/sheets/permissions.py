from rest_framework.permissions import BasePermission


class IsObjectOwnerPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if obj.creator == request.user and (view.action == 'partial_update'
                                            or view.action == 'perform_destroy'):
            return True
        if view.action == 'retrieve' or view.action == 'list':
            return True
        else:
            return False
