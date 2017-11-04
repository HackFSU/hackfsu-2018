"""
    Upload college school data to db from csv
    COUNTRY,SCHOOL_NAME,WEBSITE
"""

from api.models import School
import csv


DATA_CSV = './scripts/data/world-universities.csv'
COL_COUNTRY = 0
COL_SCHOOL_NAME = 1
COL_SCHOOL_URL = 2


def read_schools(country):
    schools = list()
    with open(DATA_CSV, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[COL_COUNTRY] == country:
                schools.append((row[COL_SCHOOL_NAME], row[COL_SCHOOL_URL]))
    print('Read {} schools'.format(len(schools)))
    return schools


def save_schools(schools):
    save_count = 0
    for school in schools:
        if not School.objects.filter(name=school[0]).exists():
            new_school = School(
                name=school[0],
                url=school[1],
                type='C',
                user_submitted=False
            )
            new_school.save()
            save_count += 1
    print('Saved {} new schools'.format(save_count))


def run():
    schools = read_schools('US')
    save_schools(schools)
    print(School.objects.count() + ' total schools in database')


if __name__ == '__main__':
    run()
