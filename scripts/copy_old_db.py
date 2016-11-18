"""

Copies desired data from a copy of the old HackFSU-2016 parse database

Uses the app api debug paths

"""

from pprint import pprint
import requests
import json

SERVER_ROOT_URL = 'http://localhost:8000'
DB_ROOT = './data/parse-2016/'
HACKATHON_ID = 3
CACHE = {}


def post_json(url, data):
    return requests.post(url, {
        'data': json.dumps(data)
    }).json()


def push_model(model_name, data):
    pprint(post_json(SERVER_ROOT_URL + '/api/debug/save', {
        'model_name': model_name,
        'data': data
    }))


def load(parse_class):
    if parse_class == 'User':
        parse_class = '_' + parse_class

    if parse_class in CACHE:
        return CACHE[parse_class]

    with open(DB_ROOT + parse_class + '.json') as file:
        rows = json.load(file)['results']
        CACHE[parse_class] = rows
        return CACHE[parse_class]


def user_id(users, user_object_id):
    pass


def is_user(parse_obj, pointer_key, user):
    return pointer_key in parse_obj and parse_obj[pointer_key]['objectId'] == user['objectId']


def is_mentor(user):
    for mentor in load('Mentor'):
        if is_user(mentor, 'user', user):
            return True
    return False


def is_judge(user):
    for judge in load('Judge'):
        if is_user(judge, 'user', user):
            return True
    return False


def is_hacker_attendee(user):
    for hacker in load('Hacker'):
        if is_user(hacker, 'user', user) and 'status' in hacker and hacker['status'] == 'checked in':
            return True
    return False


def save_hackathon():
    """ Gets totals and saves old hackathon stats """
    attendee_shirt_sizes = {}
    anon_stats = {}
    hacker_attendees = 0

    for user in load('User'):
        if is_judge(user) or is_mentor(user):
            size = user['shirtSize']
            if size not in attendee_shirt_sizes:
                attendee_shirt_sizes[size] = 0
            attendee_shirt_sizes[size] += 1

        elif is_hacker_attendee(user):
            size = user['shirtSize']
            if size not in attendee_shirt_sizes:
                attendee_shirt_sizes[size] = 0
            attendee_shirt_sizes[size] += 1
            hacker_attendees += 1

    for stat in load('AnonStat'):
        name = stat['name']
        value = stat['option']
        if name not in anon_stats:
            anon_stats[name] = {}
        if value not in anon_stats[name]:
            anon_stats[name][value] = 0
        anon_stats[name][value] += 1

    hackathon = {
        'id': HACKATHON_ID,
        'judges': len(load('Judge')),
        'mentors': len(load('Mentor')),
        'hackers_registered': len(load('Hacker')),
        'hackers_rsvp': len(load('Confirmation')),
        'hackers_attended': hacker_attendees,
        'attendee_shirt_sizes': attendee_shirt_sizes,
        'anon_stats': anon_stats
    }

    pprint(hackathon)
    push_model('Hackathon', hackathon)


def save_subscribers():
    subscribers = load('Subscriber')

    for subscriber in subscribers:
        subscriber['hackathon'] = HACKATHON_ID


def save_users():
    parse_users = load('_User')

    for user in parse_users:
        pass

    return {}


def save_hackers(users):
    hacker_old = load('Hacker')


def save_mentors(users):
    mentor_old = load('Mentor')


def save_hacks(users):
    hacks = load('Hack')


def save():
    save_hackathon()
    # user = save_users()
    # save_hackers(users)
    # save_mentors(users)
    # save_hacks()


if __name__ == '__main__':
    save()
