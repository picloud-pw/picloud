from functools import wraps

from django.http import JsonResponse


def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return JsonResponse({"error": "User is not authorized."})
        return view(*args, **kwargs)
    return wrapper
