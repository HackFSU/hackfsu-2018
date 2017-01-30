from hackfsu_com.util import email
from api.models import UserInfo


def run():
    unassigned = UserInfo.objects.filter(user__attendeestatus__isnull=True)

    print('Found {} unassigned users'.format(unassigned.count()))

    for user_info in unassigned:
        email.send_template(
            to_email=user_info.user.email,
            to_first_name=user_info.user.first_name,
            to_last_name=user_info.user.last_name,
            template_name='unassigned_register_reminder',
            subject='Your HackFSU Registration is Incomplete'
        )
        print('Email sent to ' + user_info.user.email)

    print('\n{} Total emails sent'.format(unassigned.count()))

