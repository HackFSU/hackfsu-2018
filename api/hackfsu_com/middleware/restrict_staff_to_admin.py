from django.core.urlresolvers import reverse
from django.http import Http404


class RestrictStaffToAdminMiddleware(object):
    """
        Unauthorized access to admin page will prevent access, not just direct them to django login
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    @staticmethod
    def process_request(request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated():
                if not request.user.is_staff:
                    raise Http404
            else:
                raise Http404
