"""
    Custom view decorators
"""
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def require_POST_JSON(view_function):
    @require_POST
    def wrap(request):
        try:
            request.JSON
        except NameError:
            return JsonResponse({
                'error': 'ContentType "application/json" required.'
            })
        return view_function(request)
    return wrap
