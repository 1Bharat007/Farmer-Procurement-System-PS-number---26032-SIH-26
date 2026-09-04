from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class PhoneOrUsernameAuthBackend(ModelBackend):
    """
    Authenticate using either phone_number or username with password.
    Supports staff, operators, and admin login.
    """
    def authenticate(self, request, username=None, password=None, phone_number=None, **kwargs):
        UserModel = get_user_model()
        identifier = phone_number or username or kwargs.get('phone')

        if not identifier:
            return None

        clean_id = str(identifier).strip().replace(" ", "").replace("-", "")
        if clean_id.startswith("+91"):
            clean_id = clean_id[3:]

        try:
            # Query by phone_number
            user = UserModel.objects.filter(
                Q(phone_number=clean_id) | Q(phone_number=str(identifier).strip())
            ).first()

            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None

        return None
