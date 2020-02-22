from django.contrib.auth.models import User

from .constants import ALLOW_VIEW_SELECTION

def check_if_is_supervisor(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return False
    return user.username in ALLOW_VIEW_SELECTION
