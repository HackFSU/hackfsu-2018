"""
    Submits grades for a hack
"""


from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import JudgeInfo, JudgingAssignment, JudgingCriteria, JudgingGrade, Hackathon


class RequestForm(forms.Form):
    judging_assignment_id = forms.IntegerField()
    criteria_grades = JsonField()                   # Array of tuples [[criteria_id, grade]]


class SubmitGradesView(ApiView):
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])
    request_form_class = RequestForm

    def work(self, request, req, res):
        hackathon = Hackathon.objects.current()

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

        pending_grades = []

        # Parse grades, validating along the way
        given_grades = req['criteria_grades']
        # if type(given_grades) is not list:
        #     raise ValidationError('Must be array, is type ' + type(given_grades), params='criteria_grade')

        # Split up array
        grade_tuples = []
        curr = 1
        curr_grade = []
        for entry in given_grades.split(','):
            curr_grade.append(int(entry))
            if curr % 2 == 0:
                # Complete it
                grade_tuples.append(curr_grade)
                curr_grade = []
            curr += 1

        if len(grade_tuples) == 0:
            raise ValidationError('Bad grade parse')

        for given_grade in grade_tuples:
            # if type(given_grade) is not list or \
            #         len(given_grade) != 2 or \
            #         type(given_grade[0]) is not int or \
            #         type(given_grade[1]) is not int:
            #     raise ValidationError('Must be array of tuples (id, grade), is array of ' + type(given_grade),
            #                           params='criteria_grade')
            criteria_id = given_grade[0]
            try:
                criteria = JudgingCriteria.objects.get(id=criteria_id)
            except JudgingCriteria.DoesNotExist:
                raise ValidationError('Invalid criteria id ' + criteria_id)
            pending_grades.append(JudgingGrade(
                hackathon=hackathon,
                by_judge=judge,
                hack=assignment.hack,
                criteria=criteria, grade=given_grade[1]
            ))

        # Complete assignment
        assignment.status = JudgingAssignment.STATUS_COMPLETE
        assignment.save()

        # Save the grades
        for grade in pending_grades:
            grade.save()

