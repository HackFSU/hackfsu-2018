"""
    Hack judging

    GET : get a set of hacks to judge and available superlatives
    POST : submit ranking of hacks and superlative nominations
"""

from django import forms
from django.db.models import Count
from django.http.request import HttpRequest
from django.core.exceptions import ValidationError

from api.models import Hackathon, Hack, JudgingExpo, JudgeInfo
from api.models.judging_criteria import JudgingCriteria
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from hackfsu_com.views.generic import ApiView

import logging


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
    expo = JsonField()


class RequestForm(forms.Form):
    order = JsonField()
    superlatives = JsonField()


class GetHacksView(ApiView):
    http_method_names = ['get']  # Override to allow GET
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        judge = JudgeInfo.objects.get(hackathon=current_hackathon, user=request.user)

        # Tracker for whether the judge/device has a pending assignment
        judge_hack_assignment = list(Hack.objects.with_active_judge(judge)
            .values_list('table_number', flat=True))
        has_active_assignment = len(judge_hack_assignment) is not 0

        logging.warn('incoming judge hack assignment: ' + str(judge_hack_assignment))

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
                .order_by('times_judged', 'num_judges')[:3]
            judge_hack_assignment = list(hacks.values_list('table_number', flat=True))

            # Add judge to hack's active judges
            for table_num in judge_hack_assignment:
                hack = Hack.objects.from_table_number(table_num)
                hack.current_judges.add(judge)

        superlative_categories = JudgingCriteria.objects.all()

        logging.warn('outgoing judge hack assignment: ' + str(judge_hack_assignment))

        res['hacks'] = judge_hack_assignment
        res['superlatives'] = list(superlative_categories.values_list('name', flat=True))
        res['expo'] = JudgingExpo.objects.current(hackathon=current_hackathon).name

class PostHacksView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.group_judge])

    def work(self, request: HttpRequest, req: dict, res: dict):
        current_hackathon = Hackathon.objects.current()
        judge = JudgeInfo.objects.get(hackathon=current_hackathon, user=request.user)

        # Tracker for whether the judge/device has a pending assignment
        judge_hack_assignment = list(Hack.objects.with_active_judge(judge)
            .values_list('table_number', flat=True))
        has_active_assignment = len(judge_hack_assignment) is not 0

        # If POST, make sure the data fits the hacks they were assigned.
        # Accept the ratings for the hacks they received.
        if has_active_assignment:
            order = get_order(req)

            logging.warn('incoming score submissions: ' + str(order.values()))
            logging.warn('the assignment was: ' + str(judge_hack_assignment))

            # If the hacks they sent back match their assignment...
            if set(order.values()) == set(judge_hack_assignment):

                # ... accept scores ...
                for rank, table in order.items():
                    hack = Hack.objects.from_table_number(table)
                    hack.total_judge_score += int(rank)
                    hack.save()

                # ... annotate superlatives ...
                nominations = get_superlatives(req)
                for table, superlative_names in nominations.items():
                    hack = Hack.objects.filter(table_number=table).first()
                    for name in superlative_names:
                        superlative = JudgingCriteria.objects.filter(name=name).first()
                        hack.nomination_set.create(superlative=superlative)

                # ... and remove judge from assignments
                for table_num in judge_hack_assignment:
                    hack = Hack.objects.from_table_number(table_num)
                    hack.current_judges.remove(judge)
                    hack.judges.add(judge)
                    # hack.save()

            else:
                raise ValidationError('These are the wrong tables', params=['order'])

        else:
            raise ValidationError('You don\'t have an assignment.')
