"""
    Uploads hackers teams into system. Does not insert if team name already in db (can update by re-running script!)
"""


from django.conf import settings
from api.models import Hackathon, Hack, JudgingCriteria
import os, sys
import csv

INPUT_FILE_PATH = os.path.join(settings.BASE_DIR, './scripts/data/devpost_submissions.csv')

H = Hackathon.objects.current()

COL_HACK_NAME = 0
COL_HACK_DESCRIPTION = 2
COL_HACK_OPT_IN_CRITERIA = 6


def parse_criteria(criteria_name: str) -> JudgingCriteria:
    try:
        return JudgingCriteria.objects.get(hackathon=H, name=criteria_name)
    except JudgingCriteria.DoesNotExist as e:
        print('Invalid criteria name "{}"'.format(criteria_name))
        raise e


def parse_opt_in_list(opt_ins: str) -> list:
    criteria = []
    for name in opt_ins.split(','):
        name = name.strip()
        if len(name) > 0:
            criteria.append(parse_criteria(name))
    return criteria


def read_hacks_from_csv() -> list:
    hacks = []
    with open(INPUT_FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        row_num = 0
        for row in reader:
            row_num += 1
            if row_num == 1:
                # Ignore header line
                continue

            col_num = 0
            hack = {}
            for col in row:
                if col_num == COL_HACK_NAME:
                    hack['name'] = col
                elif col_num == COL_HACK_DESCRIPTION:
                    hack['description'] = col
                elif col_num == COL_HACK_OPT_IN_CRITERIA:
                    hack['opt_in_list'] = col
                col_num += 1

            hacks.append(hack)
    return hacks


def save_hack_if_new(hackDict: Hack) -> bool:
    if Hack.objects.filter(hackathon=H, name=hackDict['name']).exists():
        return False

    hack = Hack.objects.create(
        hackathon=H,
        name=hackDict['name'],
        description=hackDict['description'],
        table_number=Hack.objects.get_next_table_number()
    )

    # for criteria in parse_opt_in_list(hackDict['opt_in_list']):
    #         hack.extra_judging_criteria.add(criteria)

    hack.save()
    return True


def run():
    total = 0
    hacks = read_hacks_from_csv()
    for hack in hacks:
        if save_hack_if_new(hack):
            total += 1
    print('Saved {} new hacks of {} hacks in file'.format(total, len(hacks)))
