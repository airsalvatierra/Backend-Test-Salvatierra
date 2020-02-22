from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect

from comun.utils import check_if_is_supervisor


def get_request(args):
    for arg in args:
        if isinstance(arg, WSGIRequest):
            return arg
    return None


def is_supervisor_or_redirect(function):
    def new_function(*args, **kwargs):
        request = get_request(args)
        result = check_if_is_supervisor(request.user.username)
        if not result:
            messages.warning(
                request,
                'No authorized, redirected to home page'
            )
            return redirect('home')
        return function(*args, **kwargs)
    return new_function
