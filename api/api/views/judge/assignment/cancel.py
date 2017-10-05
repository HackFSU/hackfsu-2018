"""
    Cancels an assigned assignment
"""


from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import JudgeInfo, JudgingAssignment


class RequestForm(forms.Form):
    judging_assignment_id = forms.IntegerField()


class CancelView(ApiView):
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])
    request_form_class = RequestForm

    def work(self, request, req, res):

        # Make sure can submit assignment
        try:
            assignment = JudgingAssignment.objects.get(id=req['judging_assignment_id'])
        except JudgingAssignment.DoesNotExist:
            raise ValidationError('Invalid assignment id')
        if assignment.status != JudgingAssignment.STATUS_PENDING:
            raise ValidationError('Assignment is not pending')

        # Make sure assigned judge
        try:
            judge = JudgeInfo.objects.get(user=request.user)
        except JudgeInfo.DoesNotExist:
            raise ValidationError('Invalid user. Missing judge object')
        if assignment.judge != judge:
            raise ValidationError('Judge user not assigned to this assignment')

        # Cancel assignment
        assignment.status = JudgingAssignment.STATUS_CANCELED
        assignment.save()


