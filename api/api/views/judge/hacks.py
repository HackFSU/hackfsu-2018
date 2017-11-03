"""
    Hack judging

    GET : get a set of hacks to judge and available superlatives
    POST : submit ranking of hacks and superlative nominations
"""

from django import forms
from django.http.request import HttpRequest

from api.models import Hackathon, Hack, JudgingExpo, JudgeInfo
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from hackfsu_com.views.generic import ApiView


class ResponseForm(forms.Form):
    hacks = JsonField()
    superlatives = JsonField()


class RequestForm(forms.Form):
    order = JsonField()
    superlatives = JsonField()


class HacksView(ApiView):
    http_method_names = ['post', 'get']        # Override to allow GET
    response_form_class = ResponseForm
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge, acl.group_pending_judge])

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        judge = JudgeInfo.objects.get(hackathon=current_hackathon, user=request.user)

        # Tracker for whether the judge/device has a pending assignment
        judge_hack_assignment = Hack.get_active_hacks_for_judge(judge)
        has_active_assignment = len(judge_hack_assignment) is not 0

        # If POST, make sure the data fits the hacks they were assigned.
        # Accept the ratings for the hacks they received.
        if has_active_assignment and request.method is 'POST':
            # TODO validate their returned hacks match the assignment

            # TODO ... accept scores if match ...

            # Remove judge from assignments
            for hack in judge_hack_assignment:
                hack.current_judges.remove(judge)
            has_active_assignment = False

        # If they don't have a hack assignment, make a new one
        if not has_active_assignment:

            # New assignment is:
            #   - 3 hacks
            #   - least judged hacks
            #   - from current expo
            hacks = Hack.objects.all().order_by('times_judged')
            current_expo = JudgingExpo.objects.current(hackathon=current_hackathon)
            judge_hack_assignment = list(filter(lambda h: h.get_expo() is current_expo, hacks))

        res['hacks'] = judge_hack_assignment
        res['superlatives'] = []
        # TODO res['superlatives'] = ???
