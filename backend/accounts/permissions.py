from rest_framework import permissions


class IsFarmer(permissions.BasePermission):
    """
    Permission check for authenticated Farmer users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # If obj is a Farmer user
        if hasattr(obj, 'phone_number'):
            return obj == request.user
        # If obj has a farmer foreign key
        if hasattr(obj, 'farmer'):
            return obj.farmer == request.user
        return False


class IsCentreOperator(permissions.BasePermission):
    """
    Permission check for authenticated Centre Operators.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'centre_operator') and request.user.centre_operator.is_active

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if not (hasattr(request.user, 'centre_operator') and request.user.centre_operator.is_active):
            return False

        operator_centre = request.user.centre_operator.centre

        # Direct ProcurementCentre instance
        if hasattr(obj, 'daily_capacity'):
            return obj == operator_centre

        # Object linked to a centre directly (e.g. Slot, OperatingHours, QueueToken)
        if hasattr(obj, 'centre'):
            return obj.centre == operator_centre

        # Object linked via slot (e.g. Booking)
        if hasattr(obj, 'slot') and hasattr(obj.slot, 'centre'):
            return obj.slot.centre == operator_centre

        return False


class IsOwnerOrCentreOperatorOrAdmin(permissions.BasePermission):
    """
    Allows:
    - Superusers / staff admins: full access
    - Centre Operators: access to objects linked to their assigned centre
    - Farmers: access strictly to their own objects
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or (user.is_staff and not hasattr(user, 'centre_operator')):
            return True

        # Check centre operator
        if hasattr(user, 'centre_operator') and user.centre_operator.is_active:
            operator_centre = user.centre_operator.centre
            if hasattr(obj, 'centre') and obj.centre == operator_centre:
                return True
            if hasattr(obj, 'slot') and hasattr(obj.slot, 'centre') and obj.slot.centre == operator_centre:
                return True
            if hasattr(obj, 'booking') and hasattr(obj.booking, 'slot') and obj.booking.slot.centre == operator_centre:
                return True

        # Check farmer ownership
        if hasattr(obj, 'farmer') and obj.farmer == user:
            return True
        if hasattr(obj, 'user') and obj.user == user:
            return True
        if obj == user:
            return True
        if hasattr(obj, 'booking') and hasattr(obj.booking, 'farmer') and obj.booking.farmer == user:
            return True

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permits read-only requests for any user, write requests only for superuser/staff.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))
