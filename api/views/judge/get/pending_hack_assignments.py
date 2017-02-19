"""
    Returns all pending hack assignments
"""


from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, JudgeInfo, JudgingAssignment


class ResponseForm(forms.Form):
    hacks = JsonField()


class PendingHackAssignmentView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        hackathon = Hackathon.objects.current()

        # Make sure valid judge
        try:
            judge = JudgeInfo.objects.get(user=request.user)
        except JudgeInfo.DoesNotExist:
            raise ValidationError('Invalid user. Missing judge object')
        if not judge.approved or judge.hackathon != hackathon:
            raise ValidationError('You are not approved to judge this hackathon')

        # Get next assigned hacks' basic info
        hacks = []
        assignments = JudgingAssignment.objects.filter(
            hackathon=hackathon,
            judge=judge,
            status=JudgingAssignment.STATUS_PENDING
        ).order_by('hack__table_number').all()[0]
        for assignment in assignments:
            hack = assignment.hack
            hacks.append({
                'assignment_id': assignment.id,
                'hack_name': hack.name,
                'hack_table_number': hack.table_number,
                'assignment_status': assignment.status
            })

        res['hacks'] = hacks
