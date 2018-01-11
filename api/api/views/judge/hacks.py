"""
    Hack judging

    GET : get a set of hacks to judge and available superlatives
    POST : submit ranking of hacks and superlative nominations
"""

from django import forms
from django.db.models import Count
from django.http.request import HttpRequest

from api.models import Hackathon, Hack, JudgingExpo, JudgeInfo
from api.models.judging_criteria import JudgingCriteria
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from hackfsu_com.views.generic import ApiView


def get_order(req: dict) -> dict:
    order = req.get('order', dict())
    if isinstance(order, dict):
        return order
    return dict()


def get_superlatives(req: dict) -> dict:
    sups = req.get('superlatives', dict())
    if isinstance(sups, dict):
        return sups
    return dict()


class ResponseForm(forms.Form):
    hacks = JsonField()
    superlatives = JsonField()


class RequestForm(forms.Form):
    order = JsonField()
    superlatives = JsonField()


class HacksView(ApiView):
    http_method_names = ['post', 'get']  # Override to allow GET
    response_form_class = ResponseForm
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge, acl.group_pending_judge])

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        judge = JudgeInfo.objects.get(hackathon=current_hackathon, user=request.user)

        # Tracker for whether the judge/device has a pending assignment
        judge_hack_assignment = Hack.objects.with_active_judge(judge)
        has_active_assignment = len(judge_hack_assignment) is not 0

        # If POST, make sure the data fits the hacks they were assigned.
        # Accept the ratings for the hacks they received.
        if has_active_assignment and request.method == 'POST':
            table_numbers = list(judge_hack_assignment.values_list('table_number', flat=True))
            order = get_order(req)

            # If the hacks they sent back match their assignment...
            if set(order.values()) == set(table_numbers):

                # ... accept scores ...
                for rank, table in order.items():
                    hack = Hack.objects.filter(table_number=table).first()
                    hack.total_judge_score += int(rank)
                    hack.save()

                # TODO ... annotate superlatives ...
                nominations = get_superlatives(req)
                for table, superlative_names in nominations.items():
                    hack = Hack.objects.filter(table_number=table).first()
                    for name in superlative_names:
                        superlative = JudgingCriteria.objects.filter(name=name).first()
                        hack.nomination_set.create(superlative=superlative)

                # ... and remove judge from assignments
                for hack in judge_hack_assignment:
                    hack.current_judges.remove(judge)
                    hack.judges.add(judge)
                has_active_assignment = False

        # If they don't have a hack assignment, make a new one
        if not has_active_assignment:
            # New assignment is:
            #   - 3 hacks
            #   - from current expo
            #   - least judged hacks
            #   - with fewest active judges
            #   - that isn't a repeat assignment
            current_expo = JudgingExpo.objects.current(hackathon=current_hackathon)
            hacks = Hack.objects.from_expo(current_expo) \
                .without_previous_judge(judge) \
                .annotate(num_judges=Count('current_judges')) \
                .order_by('times_judged', 'num_judges')
            judge_hack_assignment = hacks

            # Add judge to hack's active judges
            for hack in judge_hack_assignment:
                hack.current_judges.add(judge)

        superlative_categories = JudgingCriteria.objects.all()

        res['hacks'] = list(judge_hack_assignment.values_list('table_number', flat=True))
        res['superlatives'] = list(superlative_categories.values_list('name', flat=True))
