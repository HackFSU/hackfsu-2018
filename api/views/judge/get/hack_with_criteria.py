"""
    Return a hack with criteria to judge
"""


from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, JudgeInfo, JudgingAssignment, JudgingCriteria


def get_criteria_type_summary(criteria: JudgingCriteria) -> dict:
    return {
        'id': criteria.id,
        'name': criteria.name,
        'description_short': criteria.description_short
    }


class RequestForm(forms.Form):
    judging_assignment_id = forms.IntegerField()


class ResponseForm(forms.Form):
    hack_table_number = forms.IntegerField()
    hack_name = forms.CharField()
    overall_criteria = JsonField()
    extra_criteria = JsonField()


class HackWithCriteriaView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])
    response_form_class = ResponseForm
    request_form_class = RequestForm

    def work(self, request, req, res):
        # Make sure can submit assignment
        try:
            assignment = JudgingAssignment.objects.get(id=req['judging_assignment_id'])
        except JudgingAssignment.DoesNotExist:
            raise ValidationError('Invalid id url param')
        if assignment.status != JudgingAssignment.STATUS_PENDING:
            raise ValidationError('Assignment is not pending')

        # Make sure assigned judge
        try:
            judge = JudgeInfo.objects.get(user=request.user)
        except JudgeInfo.DoesNotExist:
            raise ValidationError('Invalid user. Missing judge object')
        if assignment.judge != judge:
            raise ValidationError('Judge user not assigned to this assignment')

        # Hack info
        res['hack_table_number'] = assignment.hack.table_number
        res['hack_name'] = assignment.hack.name

        # Criteria
        h = Hackathon.objects.current()
        res['overall_criteria'] = get_criteria_type_summary(
            JudgingCriteria.objects.filter(hackathon=h, criteria_type=JudgingCriteria.CRITERIA_TYPE_OVERALL).all()
        )
        res['extra_criteria'] = get_criteria_type_summary(assignment.hack.extra_judging_criteria.all())

