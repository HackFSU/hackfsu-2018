"""
    Accumulates all grades and gives current results
"""


from django import forms
from hackfsu_com.views.generic import ApiView
from hackfsu_com.util import acl
from hackfsu_com.util.forms import JsonField
from api.models import Hackathon, JudgingGrade, JudgingCriteria

CRITERIA_OVERALL_ID = 100


def average_criteria_result(result):
    """ Averages a single criteria section and determines point value """
    result['contribution'] = 1.0 * result['running_total'] / result['times_graded'] / 100 * result['max_contribution']


def average_criteria_results(results: dict):
    # Get point contributions for every criteria
    for type_id, grade_group in results.items():
        for result_id, criteria_result in grade_group.items():
            average_criteria_result(criteria_result)

    # Add overall grade (sum of overall criteria contributions)
    final_grade = 0.0
    for criteria_id, criteria_result in results[JudgingCriteria.CRITERIA_TYPE_OVERALL].items():
        final_grade += criteria_result['contribution']
    results[JudgingCriteria.CRITERIA_TYPE_OVERALL][CRITERIA_OVERALL_ID] = {
        'running_total': final_grade,
        'times_graded': next(iter(results[JudgingCriteria.CRITERIA_TYPE_OVERALL].values()))['times_graded'],
        'max_contribution': 100,
        'contribution': final_grade
    }


class ResponseForm(forms.Form):
    graded_hacks = JsonField()          # Array of hacks with average grades
    criteria_names = JsonField()              # { id: criteria name } for lookup


class GradesView(ApiView):
    http_method_names = ['get']
    access_manager = acl.AccessManager(acl_accept=[acl.group_organizer])
    response_form_class = ResponseForm

    def work(self, request, req, res):
        hackathon = Hackathon.objects.current()

        graded_hacks = list()
        current_hack = None
        current_hack_results = None
        for grade in JudgingGrade.objects.filter(hackathon=hackathon).order_by('hack').all():
            # print('{} {} {}'.format(grade.hack.table_number, grade.criteria.name, grade.grade))
            if current_hack != grade.hack:
                if current_hack is not None:
                    # Accumulate and save final results
                    average_criteria_results(current_hack_results)
                    # print('hack results', current_hack_results)
                    graded_hacks.append({
                        'hack': {
                            'name': current_hack.name,
                            'table_number': current_hack.table_number
                        },
                        'results': current_hack_results
                    })

                # Initialize for this next hack
                current_hack = grade.hack
                current_hack_results = {
                    JudgingCriteria.CRITERIA_TYPE_OVERALL: dict(),
                    JudgingCriteria.CRITERIA_TYPE_SUPERLATIVE: dict()
                }

            # Add grade
            grade_group = current_hack_results[grade.criteria.criteria_type]
            if grade.criteria.id not in grade_group:
                grade_group[grade.criteria.id] = {
                    'running_total': 0,
                    'times_graded': 0,
                    'max_contribution': grade.criteria.point_contribution,
                    'contribution': None    # TBD later
                }
            result = grade_group[grade.criteria.id]
            result['running_total'] += grade.grade
            result['times_graded'] += 1

        # Do last hack
        if current_hack is not None and current_hack_results is not None:
            # Accumulate and save final results
            average_criteria_results(current_hack_results)
            # print('hack results', current_hack_results)
            graded_hacks.append({
                'hack': {
                    'name': current_hack.name,
                    'table_number': current_hack.table_number
                },
                'results': current_hack_results
            })

        res['graded_hacks'] = graded_hacks

        # Map criteria id to name
        criteria_names = {
            JudgingCriteria.CRITERIA_TYPE_OVERALL: dict(),
            JudgingCriteria.CRITERIA_TYPE_SUPERLATIVE: dict()
        }
        for criteria in JudgingCriteria.objects.filter(
            hackathon=hackathon,
            criteria_type__in=[JudgingCriteria.CRITERIA_TYPE_OVERALL, JudgingCriteria.CRITERIA_TYPE_SUPERLATIVE]
        ).distinct().all():
            criteria_names[criteria.criteria_type][criteria.id] = criteria.name

        res['criteria_names'] = criteria_names

