"""
    Attempt to assign a judge the given amount of hacks. May assign 0 to given number.
"""
from django import forms
from django.core.exceptions import ValidationError
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from api.models import JudgeInfo, Hackathon, Hack, JudgingAssignment, JudgingExpo

CANCEL_THRESHOLD = 5    # If hack assignment cancel count reaches this number, it is no longer assigned


def get_sorted_possible_hacks(expo: JudgingExpo, hackathon: Hackathon, judge: JudgeInfo, max_judge_count: int):
    counted_statuses = [JudgingAssignment.STATUS_PENDING, JudgingAssignment.STATUS_COMPLETE]
    hacks_in_expo = Hack.objects.filter(
        hackathon=hackathon,
        table_number__gte=expo.table_number_start,
        table_number__lte=expo.table_number_end
    ).all()

    possible_hacks = []
    assignment_counts = {}

    for hack in hacks_in_expo:
        assignments = JudgingAssignment.objects.filter(hack=hack, status__in=counted_statuses)
        assignment_count = assignments.count()
        if assignments.count() >= max_judge_count or \
                assignments.filter(judge=judge).exists() or \
                assignments.filter(status=JudgingAssignment.STATUS_CANCELED).count() >= CANCEL_THRESHOLD:
            # Cannot judge this one
            continue
        possible_hacks.append(hack)
        assignment_counts[hack.id] = assignment_count

    # Sort ascending by least assigned (for assignment scattering purposes)
    possible_hacks.sort(key=lambda x: assignment_counts[x.id])
    return possible_hacks


class RequestForm(forms.Form):
    max_hacks = forms.IntegerField(min_value=1)             # Maximum number of hacks to assign to judge
    max_judge_count = forms.IntegerField(min_value=1)       # Maximum number of times a hack should be judged
    judge_info_id = forms.IntegerField()


class ResponseForm(forms.Form):
    new_assignments = forms.IntegerField()


class AssignHacksView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])

    def work(self, request, req, res):
        hackathon = Hackathon.objects.current()

        # Make sure valid judge
        try:
            judge = JudgeInfo.objects.get(id=req['judge_info_id'])
        except JudgeInfo.DoesNotExist:
            raise ValidationError('Invalid id', params=['judge_info_id'])
        if not judge.approved or judge.hackathon != hackathon:
            raise ValidationError('Judge is not approved for this hackathon', params=['judge_info_id'])

        # Get the current expo
        expo = JudgingExpo.objects.current(hackathon=hackathon)
        if expo is None:
            raise ValidationError('There is not an expo going on to get hacks for!')

        # Check if they still have any pending assignments
        pending_assignments = JudgingAssignment.objects.filter(
            judge=judge,
            status=JudgingAssignment.STATUS_PENDING
        ).count()
        if pending_assignments > 0:
            raise ValidationError('Judge still has pending assignments. Tell them to either cancel or grade them.')

        new_assignments = 0
        possible_hacks = get_sorted_possible_hacks(expo, hackathon, judge, req['max_judge_count'])
        for i in range(len(possible_hacks)-1):
            # Assign next
            JudgingAssignment.objects.create(hackathon=hackathon, judge=judge, hack=possible_hacks[i])
            new_assignments += 1

            if new_assignments >= req['max_hacks']:
                # Max hacks assigned, stop
                break

        res['new_assignments'] = new_assignments
