"""
    Grade an assigned hack
"""

from django.http import Http404
from hackfsu_com.views.generic import PageView
from hackfsu_com.util import acl
from api.models import JudgingAssignment


class HackPage(PageView):
    allowed_after_current_hackathon_ends = False
    template_name = 'judge/hack/index.html'
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])

    def work(self, request):
        if not JudgingAssignment.objects.filter(
            id=self.kwargs['id'],
            judge__user=request.user,
            status=JudgingAssignment.STATUS_PENDING
        ).exists():
            raise Http404()


