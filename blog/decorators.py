from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect


def author_required(view_func):
    """
    Decorator for views that checks whether the user is logged in and is an approved Author
    (or superuser). Raises PermissionDenied if not authorized.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        
        is_author = False
        if hasattr(request.user, 'author_profile') and request.user.author_profile.is_author:
            is_author = True
        elif request.user.is_superuser:
            is_author = True

        if not is_author:
            messages.error(request, "Access denied. Only approved Authors can access this area.")
            raise PermissionDenied("Author status required.")
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view
