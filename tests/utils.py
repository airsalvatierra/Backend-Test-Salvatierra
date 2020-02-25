from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

def set_base_request(request, user=None, is_logged_in=True):
    if not user:
        user = User.objects.get(username='air.salvatierra')

    if is_logged_in:
        request.user = user
    middleware = SessionMiddleware()
    middleware.process_request(request)

    middleware = MessageMiddleware()
    middleware.process_request(request)

    return request
