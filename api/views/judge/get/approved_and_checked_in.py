from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, JudgeInfo, JudgingAssignment


class ResponseForm(forms.Form):
    judges = JsonField()


class ApprovedAndCheckedInView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        judges = []

        for info in JudgeInfo.objects.filter(
            hackathon=Hackathon.objects.current(),
            approved=True,
            attendee_status__checked_in_at__isnull=False
        ):
            assignments = JudgingAssignment.objects.filter(judge=info)
            judges.append({
                'id': info.id,
                'name': '{} {}'.format(info.user.first_name, info.user.last_name),
                'assignments_pending': assignments.filter(status=JudgingAssignment.STATUS_PENDING).count(),
                'assignments_completed': assignments.filter(status=JudgingAssignment.STATUS_COMPLETE).count(),
                'assignments_canceled': assignments.filter(status=JudgingAssignment.STATUS_CANCELED).count(),
            })

        res['judges'] = judges

