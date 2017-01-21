"""
    Public api view for unrestricted access
"""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from hackfsu_com.views.generic import ApiView


class PublicApiView(ApiView):
    http_method_names = ['get']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)