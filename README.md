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
* python, python-dev
* python3.5, python3.5-dev
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

# Access Control List (ACL)
The ACL is what determines whether or not the website page or api path is accessible by a user. Once a user is logged in they gain access to different restricted pages based upon the different groups their account belongs to. In addition, accounts may be disabled which will prevent them from being logged in with but not deleting them.

* When a user cannot access a website page, they are redirected to `/user/login?accessDenied=true&path=<originalPath>`
    * If the user is already logged in, they are just redirected to `/user/profile?accessDenied=true`
* When a user cannot access an API path, the call will return a `401 Unauthorized` error in the standard API error format.

All registrations of any type must be approved/activated by an organizer or admin. Admins may only be created manually by other admins. Users may belong to more than one ACL group. For example, an organizer may also be an admin, mentor, and judge.

## ACL Groups:
* `user` - anyone logged in with an account. Has UserInfo object in db.
* `hacker` - users registered as a hacker for the current hackathon. Has HackerInfo object in db.
* `mentor` - users registered as a mentor for the current hackathon. Has MentorInfo object in db. Can answer help requests.
* `judge` - users registered as a judge for the current hackathon. Has JudgeInfo object in db. Hackers may not register as a judge for the same hackathon. Can judge hack submissions.
* `organizer` - users registered as an organizer for the current hackathon. General organizational tasks allowed such as viewing users, checking people in, and sending updates. Cannot be a hacker for the same hackathon.
* `admin` - users set as an admin by other admins. They have access to hackathon management and django administration. Cannot also be a hacker for the same hackathon. This is the same as being a django superuser, and is not a user group but a set flag.

## ACL Examples:
* [] => unrestricted
* [!user] => cannot be logged in at all.
* [user] => must be logged in and belong to the user group (any logged in user should belong to this group)
* [user,!hacker] => must be logged in and belong to the user group but not the hacker group
* [mentor] => must be logged in and belong to the mentor group.
* [admin] => must be logged in and have the admin flag set.
* [admin,mentor] => must be logged in and have either the admin flag set or belong to the mentor group.


# Website Informal SRS
Most of the pages are dynamic in nature, and rely on the API which is specified in the next section. Redirects are in the form `<MATCHING_ACL> -> <DESTINATiON>`.

## Shortcuts
There are some simple redirect paths for ease of use, specified below. The ACL of the destination page will be used for determining access, although the redirect itself is unrestricted.
* `/register` -> `/registration/user`
* `/signup` -> `/registration/user`
* `/hack` -> `/registration/hacker`
* `/mentor` -> `/registration/mentor`
* `/judge` -> `/registration/judge`
* `/organize` -> `/registration/organizer`
* `/login` -> `/user/login`

## Public Informational Pages
* `/` [] - Homepage
* `/help` [] - Help request submission page for day of

* `/hacks` [] - View submitted hacks.
    - Page may be disabled/enabled by an admin.
    - Displays the names and table numbers for each hack that has been entered into the system
    - Does NOT display winners until he day AFTER the last day of the hackathon.
* `404 Error Page` [] - Displayed when a 404 error occurs (page not found)
* `500 Error Page` [] - Displayed when a 500 error occurs (internal server error)

## User Registration pages
* `/registration/user/[?=type=(hacker|mentor|judge|organizer)]` [!user] - User registration form (account creation)
    - [user] -> `/user/profile` (logged in users will be redirected to their profile)
    - This is the only formal process to become a user
    - Upon completion, the new user is logged in and then redirected to the desired registration page (or their profile by default)
    - Requires a captcha
* `/registration/hacker` [user,!mentor,!organizer,!judge] - Hacker registration form
    - [hacker] -> `/user/hack`
    - Page may be disabled/enabled by an admin.
* `/registration/mentor` [user,!hacker] - Mentor registration form
    - [mentor] -> `/user/mentor`
    - Page may be disabled/enabled by an admin.
* `/registration/judge` [user,!hacker] - Judge registration form
    - [judge] -> `/user/judge`
    - Page may be disabled/enabled by an admin.
* `/registration/organizer` [user,!hacker] - Organizer registration form
    - [organizer] -> `/user/organize`
    - Page may be disabled/enabled by an admin.


## General User Pages
* `/user/login` [] - User Login
    - [user] -> `/user/profile`
* `/user/profile` [user] - Displays current users information, groups they belong to, and useful information and links
    - Can view/edit UserInfo
        - Can change password (logs them out + redirects to `/user/login`)
        - Can change email (logs them out + redirects to `/user/login`)
            - New email may not already be connected to an existing account
    - [hacker] Can view/edit their HackerInfo
    - [mentor] Can view/edit their MentorInfo
    - [judge] Can view/edit their JudgeInfo
    - Can see any pending status change for the current hackathon
* `/user/forgot_password` [!user] - Password reset form for non-users
* `/user/confirm_email/?email=<USER_EMAIL>&code=<CONFIRMATION_CODE>` [] - Email confirmation page
    - Success? User is redirected to `/user/login`
    - Failure? Error message is displayed.
    - Emails may be only confirmed ONCE. Any subsequent attempts will be treated as a failure

## General Paths:
* `/user/organizers` [user] - Lists organizers for the current hackathon and a way to contact them if applicable
* `/user/hack` [hacker] - ??? TODO
    - Maybe this page can display general tips and hackathon info
* `/user/mentor` [mentor] - Displays pending help requests which mentors can manage
    - Can assign a help request to themselves
    - Can un-assign a help request to themselves
    - Can view all help requests for the current hackathon
    - Help request data is automatically updated via web sockets, so mentors can just keep this page open without refreshing it.
* `/user/judge` [judge] Displays assigned hacks to judge
    - Displays assigned hacks with forms to submit their opinions
    - Up to five hacks are given to judges at one time. This is acts as a 'round'
    - They must give each hack an overall score (0-5 with 5 as the best) and then may choose to give it a point towards one or more categories
    - Once they submit their round they may NOT go back and change their submissions
    - Judging works through a series of rounds until every hack has been seen at least 3 times or an organizer has stopped the judging.
    - To receive a new round a judge must go to the organizer table and ask to be assigned one.
    - At the end of all judging (as determined by the organizers), the top 10 or so of the hacks (based on overall score) will be released. The final winners will be determined manually by the final judges during the closing ceremony.
* `/user/organize` [organizer] - Displays some general how-to information for organizers with useful links.

### Organizer paths
Must be either an organizer for the current hackathon or an admin to access any of these pages.
* `/user/organize/users` [organizer] - User management.
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
* `/user/organize/user/<USER_ID>` [organizer] - Single user management.
    - Manage a single user's account.
    - Can do everything `/user/organize/users` can do and more
        - Can add notes to the account
        - Can disable and an account (prevents login)
        - Can re-enable a disabled account.
    - Displays full user information, including past hackathon history.
* `/user/organize/updates` [organizer] - Update management.
    - Displays information about updates for the current hackathon.
    - Can send updates for the current hackathon. This may or may not trigger a push notification on the apps, depending the setting.
* `/user/organize/stats` [organizer] - Displays hackathon stats for current and past hackathons
    - Can see anonymous statistics
    - Only current hackathon stats are calculated, past hackathon stats are just retrieved.
* `/user/organize/hacks` [organizer] - Hack Submission Management
    - Add/update hacks from Devpost (upload .CSV from devpost)
    - View hacks in the system including their table number, name, participants, and current judge results
    - View judges and assign them rounds
        - These rounds are just automatically generated based on what has and has not been judged.
        - Rounds can continue to be assigned until all hacks have been seen exactly three times.
    - Can download a roster that can be printed or emailed so that sponsors can use them in their judging process
    - Can start an expo for hacks x to y
    - Can end an expo
        - Will be warned if any judges still have rounds to complete

### Administration Pages
These pages are used to manage the website as a whole, so that the server does not have to be directly edited.
* `/user/admin/django` [admin] - Django administration page. Can edit database directly so use with caution.
    - Since it not done often, just manage hackathon list with this
    - Can be used to set user passwords
* `/user/admin/hackathons` [admin] - Hackathon management
    - Can set the current hackathon. The previous hackathon's statistics will be calculated and stored.
* `/user/admin/website` [admin] - Website Management
    - Can enable/disable registration pages
    - Can enable/disable day-of index page
    - Can enable/disable help submission page `/help`
    - Can enable/disable hack page


# API Informal SRS
A list of all requests handled by the api in the format `<REQUEST_TYPE> <REQUEST_PATH> <ACL> - <DESCRIPTION>`.

## General
* GET `/api/hackathon/schedule/get` [] - Returns current hackathon's schedule items in a list
* GET `/api/hackathon/sponsors/get` [] - Returns current hackathon's public sponsor list with logo image links
* GET `/api/hackathon/stats/get` [] - Returns current hackathon's public statistics
* POST `/api/hackathon/subscribe` [] - Subscribes an email for updates about the current hackathon

## User management
* POST `/api/user/login` [!user] - Logs in a user for the session
    * Must be a existing, enabled, email verified user.
* POST `/api/user/initialize_password_reset` [!user] - Sends a password reset email with a link for reset page
* POST `/api/user/finalize_password_reset` [!user] - Completes a password reset, setting a new password for the user
* GET `/api/user/profile` [user] - Returns profile data of logged in user (can handle non-user info properties as well if applicable)
* POST `/api/user/change_password` [user] - Changes user password and logs user out
* POST `/api/user/edit` [user] - Changes user properties (can handle non-user info properties as well if applicable)
* POST `/api/user/resend_email_confirmation` [!user] - Resends the email confirmation email for the account creation process
* POST `/api/user/confirm_email` [!user] - Submits an email confirmation for a pending user
* POST `/api/user/register/hacker` [!user] - Hacker new account registration
    * Email confirmation required
* POST `/api/user/register/judge` [!user] - Judge new account registration
* POST `/api/user/register/mentor` [!user] - Mentor new account registration
* POST `/api/user/register/organizer` [!user] - Organizer new account registration
* POST `/api/user/join/hackers` [user,!hacker] - Register current account for hacker status
* POST `/api/user/join/organizers` [user,!organizer] - Register current account for organizer status
* POST `/api/user/join/judges` [user,!judge] - Register current account for judge status
* POST `/api/user/join/mentors` [user,!mentor] - Register current account for mentor status

## Mentor
* GET `/api/mentor/get_requests` [mentor] - Returns all of the help requests for the current hackathon
* POST `/api/mentor/claim_request` [mentor] - Claims a help request
* POST `/api/mentor/release_request` [mentor] - Releases a claimed help request for other mentors

## Judge
TODO

## Organize
TODO

## Administration
TODO


# Project Structure
This project basic structure is that of a Django project, but it does not exactly follow all the 'Django' ways of doing things. The project is split up into two main sections, the API and the webapp.

## API
The API is the main powerhouse of any backend service call, including the managment of all the data modules. The Django Webapp, iOS app, and Android app all use this same API for accessing and managing the application data.

## Webapp
The webapp serves the front-end templates. Page content is dynamically populated via AJAX calls to the API.

If you take a look into the `/webapp/` folder you will see many different types of files. If you are unfamiliar with ANY of these technologies, please learn them via their respective documentation BEFORE working on this website. You can ask someone for help if you are having trouble, though it is recommended that you read through their docs a bit first. They docs are pretty good, and the tools are fairly simple once you get the hang of them.
    * [Sass](http://sass-lang.com/) files, `*.scss`, are used to create Cascading Style Sheet (CSS) files. We use this because Sass is an awesome tool that allows for nesting, variables, math, importing other sass files, and much more.
        * In addition to Sass, we use the [AutoPrefixer](https://autoprefixer.github.io/) tool in our build step so you don't have to worry that much about browser incompatibilities
    * [Pug](https://pugjs.org) (formally known as Jade) files, `*.pug`, are used to create Hypertext Markup Language (HTML) files. We use these as HTML template files so that we can make pages that are consistent, easy to write, and easy to read. We make extensive use of pug variables, extension, and blocks in order to abstract out most of the repetitive tasks required when adding/editing new pages, which allows us to focus on just the page content. This is a custom setup that has been found effective.
        * **Note** Django does indeed have its [own templating system](https://docs.djangoproject.com/en/1.10/topics/templates/#the-django-template-language), which is actually still being used. There is a pug engine that we could replace it with to have it compile entirely in django, but it does not have all the necessary support as its main JavaScript compiler. However, we can still allow the backend view to modify the HTML by writing unbuffered django templating language constructs directly in the pug files (just be careful).
    * Python files, `*.py`, are the backend files used to serve the templated HTML files. These will be pretty small in most cases, and you should not touch these unless you are changing the backend.

The `webapp/views` folder acts as a base for all views and corresponds to different URL paths. For example `/index.pug` is the pug template for path `/` and `/registration/hacker/index.pug` is the pug template for path `/registration/hacker/`.

For each path, the `index.pug`, `script.js`, and `style.scss` files are all kept in the same directory to keep things simple. Keeping page-specific source files in one place is better than separating them by file type (like `/js/views/registration/hacker/script.js` and `/css/views/registration/hacker/style.js`) because with many views there just gets to be so many mirrored directories, breeding errors and annoyances. With a sophisticated front-end builder like Gulp, we can automatically place the generated JS, CSS, and HTML files where they need to go but still keep the like-minded source files together.

### Building
The `.scss`, `.js`, and `.pug` built using Gulp, a very handy task runner. Gulp has been setup in this project to adhere to the following rules:
* `.scss` files will be compiled, then auto-prefixed to `.css` files into the build folder to be accessed as static files (like `/static/view/registration/hacker/style.css`)
* `.js` files will be [uglified](http://lisperator.net/uglifyjs/) and copied into the build folder to be accessed as static files (like `/static/view/registration/hacker/script.js`)
* `.pug` files will be compiled to `.html` files into the build folder to be accessed as Django template files (like `registration/hacker/index.html`)
* Files or folders starting with an underscore (`_`) will not be built by Gulp. This is particularly useful for pug/sass files that are just used to compile other pug/sass files by their respective compilers.

The JS/CSS files must be accessed by the HTML pages using absolute paths from the Django static folder, `/static/`. If your page is 404'ing on a static resource be sure to check if the path is correct and that it was actually built (if it needed to)

Files located in the `/static/` project folder are not compiled and can be accessed as-is. Use this for images and other non-compiled files.

# TODO
* Page alerts
    - Backend can trigger the creation of alerts that appear at the top of the page, and are dismissable
    - Use the Bootstrap alert classes
    - Should be very simply to add to any page
    - Could be session-based and appended automatically?
        - May need to set up a pending alerts model
    - Could be dynamically added instead
* ACL enforcement
    - Should be done with a custom view class
* Add Django template support functions to Pug
    - Should be as minimal as possible as to keep it as pug-like as possible
    - Something like `django('some_var')` should compile down to `{{ some_var }}`
    - If/else construct support would be nice as well
    - Might be able to just put in raw, unbuffered text as an option too
