"""
    View a single help request
"""

from django.http import Http404
from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl
from api.models import HelpRequest


class RequestPage(PageView):
    template_name = 'mentor/request/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_mentor])

    def work(self, request):
        if not HelpRequest.objects.filter(id=self.kwargs['id']).exists():
            raise Http404()


