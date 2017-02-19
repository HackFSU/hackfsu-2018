"""
    Get public hack roster
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, Hack, JudgingCriteria


class ResponseForm(forms.Form):
    hacks = JsonField()


class HacksWithCriteriaView(ApiView):
    http_method_names = ['get']
    response_form_class = ResponseForm

    def work(self, request, req, res):
        hacks = []
        for hack in Hack.objects.filter(hackathon=Hackathon.objects.current()):
            criteria_names = []
            for criteria in hack.extra_judging_criteria.filter(status=JudgingCriteria.CRITERIA_TYPE_MANUAL)\
                    .order_by('id').all():
                criteria_names.append(criteria.name)
            hacks.append({
                'table_number': hack.table_number,
                'name': hack.name,
                'expo': hack.get_expo_name(),
                'criteria': ', '.join(criteria_names)
            })
        res['hacks'] = hacks
