from django.core.exceptions import PermissionDenied

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'owner':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper