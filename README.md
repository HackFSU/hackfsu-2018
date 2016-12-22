HackFSU Website
===============

Remake of previous node version for 2017, now written in Django.

# Contributing
## Development Requirements
### Running front-end demo
* nodejs 6.x

Run the demo. Does not access real server, just a mock express one.
```bash
$ npm install
$ npm run demo
```


### Running full server
* a copy of `./hackfsu_com/secret_keys.json` (get from someone)
* python3.5
* pip3.5
* virtualenv
* nodejs 6.x

Setup virtualenv (do once)
```bash
$ virtualenv -p /path/to/python3.5 /path/to/repo/venv
```

Update virtualenv (do every time requirements changes)
```bash
$ ./venv/bin/pip3.5 install -r requirements.txt
```

Build frontend with npm
```bash
$ npm intall
$ npm run build
```

Run server in virtualenv
```bash
$ ./venv/bin/python manage.py runserver 8000

```

Make these tasks easier by using PyCharm and setting up run commands.


# Server deployment
Push an update to live, then run a deploy. Server access required.

The deploy script makes updating the server easy. This assumes it has already
been setup on the server. See Jared for server setup guide.
```
$ git push origin master
$ git push origin master:live
$ ssh hackfsu.com
[hackfsu]$ sudo /root/deploy.sh
```

# Website Informal SRS
Website pages people can access. In the format "`<path>` -> `<django view path>`". Most of the pages are dynamic in nature, and rely on the django API which is specified in the next section. Access to the api paths and certain pages is determined by the django session and the level of access granted via the Access Control List (ACL) and the different ACL groups that a logged in user may belong to.

## General public pages
Anyone can access these. Pages with forms will require a captcha submission as well. Registration pages can be disabled/enabled by admins.
* `/` -> `index` - Homepage
* `/help` -> `help` - Help request submission page for day of
* `/register` -> `register` - Hacker registration form (Creates new user)
    - Page may be disabled/enabled by an admin.
    - Logged in users will be redirected to `/user/hack`
* `/mentor` -> `mentor` - Mentor registration form (Creates new user)
    - Page may be disabled/enabled by an admin.
    - Logged in users will be redirected to `/user/mentor`
* `/judge` -> `judge` - Judge registration (Creates new user)
    - Page may be disabled/enabled by an admin.
    - Logged in users will be redirected to `/user/judge`
* `/organize` -> `organize` - Organizer registration (Creates new user)
    - Page may be disabled/enabled by an admin.
    - Logged in users will be redirected to `/user/organize`
* `/login` or `/user/login` -> `user/login` - User Login
    - Logged in users will be redirected to `/user/profile`
* `/hacks` -> `hacks` - View submitted hacks.
    - Page may be disabled/enabled by an admin.
    - Displays the names and table numbers for each hack that has been entered into the system
    - Does NOT display winners until he day AFTER the last day of the hackathon.
* `404 Error` -> `error/404` - Displayed when a 404 error occurs (page not found)
* `500 Error` -> `error/500` - Displayed when a 500 error occurs (internal server error)


## User Pages
Only logged in users can access these. Those that cannot will be redirected to `/user/login?accessDenied=true&path=<originalPath>` and upon login will be redirected back to the initial page. Users that do not meet the ACL requirements of a page will be redirected to `/user/profile?accessDenied=true` and a message will be displayed saying that they have been denied access. In addition, accounts may be disabled which will prevent them from being logged in with but not deleting them.

All registrations of any type must be approved/activated by an organizer or admin. Admins may only be created manually by other admins. Users may belong to more than one ACL group. For example, an organizer may also be an admin, mentor, and judge.

ACL Groups:
* `user` - anyone logged in with an account. Has UserInfo object in db.
* `hacker` - users registered as a hacker for the current hackathon. Has HackerInfo object in db.
* `mentor` - users registered as a mentor for the current hackathon. Has MentorInfo object in db. Can answer help requests.
* `judge` - users registered as a judge for the current hackathon. Has JudgeInfo object in db. Hackers may not register as a judge for the same hackathon. Can judge hack submissions.
* `organizer` - users registered as an organizer for the current hackathon. General organizational tasks allowed such as viewing users, checking people in, and sending updates. Cannot be a hacker for the same hackathon.
* `admin` - users set as an admin by other admins. They have access to hackathon management and django administration. Cannot also be a hacker for the same hackathon. This is the same as being a django superuser.

### General Paths:
* `/user/profile` -> `user/profile` - Displays current users information, groups they belong to, and useful information and links
    - Can change password
    - Can edit and view most submitted information (UserInfo, HackerInfo, MentorInfo, JudgeInfo)
* `/user/organizers` -> `user/organizers` - Lists organizers for the current hackathon and a way to contact them if applicable
* `/user/hack` -> `user/hack`
    * is hacker? - Displays information for current hackers
    * can become a hacker (cannot be a judge or organizer)?
        * Not registered for current hackathon? - Displays hacker registration form to apply for hacker status in the current hackathon.
        * Already registered but waiting for activation? - Displays a pending message, telling them to wait.
    * cannot become a hacker? - Access denied, redirected to `/user/profile?accessDenied=true`
* `/user/mentor` -> `user/mentor`
    * is mentor? - Displays pending help requests which they can manage
        - Can assign a help request to themselves
        - Can un-assign a help request to themselves
        - Can view all help requests for the current hackathon
        - Help request data is automatically updated via web sockets, so mentors can just keep this page open without refreshing it.
    * can become a mentor (every user can)?
        * Not registered for current hackathon? - Displays mentor registration form to apply for mentor status in the current hackathon.
        * Already registered but waiting for activation? - Displays a pending message, telling them to wait.
* `/user/judge` -> `user/judge`
    * is judge? - Displays assigned hacks to judge
        - Displays assigned hacks with forms to submit their opinions
            - Up to five hacks are given to judges at one time. This is acts as a 'round'
            - They must give each hack an overall score (0-5 with 5 as the best) and then may choose to give it a point towards one or more categories
            - Once they submit their round they may NOT go back and change their submissions
            - Judging works through a series of rounds until every hack has been seen at least 3 times or an organizer has stopped the judging.
            - To receive a new round a judge must go to the organizer table and ask to be assigned one.
            - At the end of all judging (as determined by the organizers), the top 10 or so of the hacks (based on overall score) will be released. The final winners will be determined manually by the final judges during the closing ceremony.
    * can become a judge (hackers cannot)?
        * Not registered for current hackathon? - Displays judge registration form to apply for judge status in the current hackathon.
        * Already registered but waiting for activation? - Displays a pending message, telling them to wait.
    * cannot become a judge? - Access denied, redirected to `/user/profile?accessDenied=true`
* `/user/organize` -> `user/organize`
    * is organizer? - Displays some general how-to information for organizers with useful links.
    * can become a mentor (every user can)?
        * Not registered for current hackathon? - Displays organizer registration form to apply for organizer status in the current hackathon.
        * Already registered but waiting for activation? - Displays a pending message, telling them to wait.
    * cannot become an organizer? - Access denied, redirected to `/user/profile?accessDenied=true`

### Organizer paths
Must be either an organizer for the current hackathon or an admin to access any of these pages.
* `/user/organize/users` -> `user/organize/users` - User management.
    - Can accept registrations for hackers, mentors, judges, and organizers.
    - Is admin? Can make users admins or remove admin status from users.
    - Can check in attendees for the current hackathon (hackers, mentors, judges)
    - Can view general user information
    - Can search for users
    - Can filter by hackathon and roles with checkboxes
    - Provides links to go to the management page for a single user.
    - User data is automatically updated via web sockets, so organizers can just keep this page open without refreshing it. This is particularly important during check-in, where multiple organizers will be using this page to
    - Can bulk download user data based on current search
    - Can bulk download user resumes
* `/user/organize/users/<USER_ID>` -> `user/organize/users/user` - Single user management.
    - Manage a single user's account.
    - Can do everything `/user/organize/users` can do and more
        - Can add notes to the account
        - Can disable and an account (prevents login)
        - Can re-enable a disabled account.
    - Displays full user information, including past hackathon history.
* `/user/organize/updates` -> `user/organize/updates` - Update management.
    - Displays information about updates for the current hackathon.
    - Can send updates for the current hackathon. This may or may not trigger a push notification on the apps, depending the setting.
* `/user/organize/stats` -> `user/organize/stats` - Displays hackathon stats for current and past hackathons
    - Can see anonymous statistics
    - Only current hackathon stats are calculated, past hackathon stats are just retrieved.
* `/user/organize/hacks` -> `user/organize/hacks` - Hack Submission Management
    - Add/update hacks from Devpost (upload .CSV from devpost)
    - View hacks in the system including their table number, name, participants, and current judge results
    - View judges and assign them rounds
        - These rounds are just automatically generated based on what has and has not been judged.
        - Rounds can continue to be assigned until all hacks have been seen exactly three times.
    - Can download a roster that can be printed or emailed so that sponsors can use them in their judging process
    - Can start an expo for hacks x to y
    - Can end an expo
        - Will be warned if any judges still have rounds to complete

### Admin paths
Must be an admin to access these pages.
* `/user/admin/django` - Django administration page. Can edit database directly so use with caution.
    - Since it not done often, just manage hackathon list with this
    - Can be used to set user passwords
* `/user/admin/hackathons` -> `user/admin/hackathons` - Hackathon management
    - Can set the current hackathon. The previous hackathon's statistics will be calculated and stored.
* `/user/admin/website` -> `user/admin/website` - Website Management
    - Can enable/disable registration pages
    - Can enable/disable day-of index page
    - Can enable/disable help submission page `/help`
    - Can enable/disable hack page


# API Informal SRS
TODO
