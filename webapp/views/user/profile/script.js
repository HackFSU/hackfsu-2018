(function($) {
    'use strict';

    var buttonContainer = $('#action-buttons');

    var GROUP = hackUtil.GROUP;

    function addActionButton(action) {
        var btn = $('<button class="btn btn-form"></button>');
        btn.prop('title', action.title);
        btn.prop('disabled', !!action.disabled);
        btn.text(action.text);
        btn.appendTo(buttonContainer);
        btn.wrap('<a href="'+action.url+'"></a>');
    }

    function initActionButtons(groups, rsvpConfirmed) {
        if (!rsvpConfirmed && (
            groups.includes(GROUP.hacker) ||
            groups.includes(GROUP.mentor) ||
            groups.includes(GROUP.judge) ||
            groups.includes(GROUP.organizer))) {

            addActionButton({
                'text': 'RSVP!',
                'url': '/user/rsvp'
            });
        }


        if (!groups.includes(GROUP.hacker) &&
            !groups.includes(GROUP.pending_hacker)) {

            if (!groups.includes(GROUP.organizer) &&
                !groups.includes(GROUP.pending_organizer) &&
                !groups.includes(GROUP.judge) &&
                !groups.includes(GROUP.pending_judge)) {

                addActionButton({
                    'text': 'Register as a hacker',
                    'url': '/registration/hacker'
                });
            }

            if (!groups.includes(GROUP.mentor) &&
                !groups.includes(GROUP.pending_mentor)) {

                addActionButton({
                    'text': 'Register as a mentor',
                    'url': '/registration/mentor'
                });
            }

            if (!groups.includes(GROUP.judge) &&
                !groups.includes(GROUP.pending_judge)) {

                addActionButton({
                    'text': 'Register as a judge',
                    'url': '/registration/judge'
                });
            }

            if (!groups.includes(GROUP.organizer) &&
                !groups.includes(GROUP.pending_organizer)) {

                addActionButton({
                    'text': 'Register as a organizer',
                    'url': '/registration/organizer'
                });
            }
        } else if (!groups.includes(GROUP.mentor) &&
            !groups.includes(GROUP.pending_mentor)) {

            addActionButton({
                'text': 'Register as a mentor',
                'url': '/registration/mentor'
            });
        }

        if (groups.includes(GROUP.mentor)) {
            addActionButton({
                'text': 'Mentor',
                'url': '/mentor'
            });
        }

        if (groups.includes(GROUP.organizer)) {
            addActionButton({
                'text': 'Django Admin Panel',
                'url': '/admin/django'
            });

            addActionButton({
                'text': 'Organize',
                'url': '/organize/'
            });
        }
    }

    function initHackathonSection(hackathonData, groups, rsvpConfirmed) {
        var section = $('#hackathon');
        var start = moment(hackathonData.hackathon_start, 'YYYY-MM-DD');
        var end = moment(hackathonData.hackathon_end, 'YYYY-MM-DD');

        var groupString = hackUtil.getNiceGroupList('You are', groups);

        if (rsvpConfirmed) {
            groupString += ' You have also RSVP\'d for this hackathon!';
        }

        // Account for not allowed data (-1)
        var i;
        for (i in hackathonData) {
            if (hackathonData.hasOwnProperty(i) && hackathonData[i] === -1) {
                hackathonData[i] = 'N/A';
            }
        }

        section.children('h1').text(hackathonData.hackathon_name);
        section.children('h3').text(start.format('MMM Do') + ' - ' + end.format('MMM Do'));
        section.children('h4').text(groupString);
        section.children('table').html(
            '<thead>' +
                '<tr>' +
                    '<th></th>' +
                    '<th>Registered</th>' +
                    '<th>Approved</th>' +
                    '<th>Checked-in</th>' +
                '</tr>' +
            '</thead>' +
            '<tbody>' +
                '<tr>' +
                    '<th>Hackers</th>' +
                    '<td>' + hackathonData.hackers_registered + '</td>' +
                    '<td>' + hackathonData.hackers_approved + '</td>' +
                    '<td>' + hackathonData.hackers_checked_in + '</td>' +
                '</tr>' +
                '<tr>' +
                    '<th>Mentors</th>' +
                    '<td>' + hackathonData.mentors_registered + '</td>' +
                    '<td>' + hackathonData.mentors_approved + '</td>' +
                    '<td>' + hackathonData.mentors_checked_in + '</td>' +
                '</tr>' +
                '<tr>' +
                    '<th>Judges</th>' +
                    '<td>' + hackathonData.judges_registered + '</td>' +
                    '<td>' + hackathonData.judges_approved + '</td>' +
                    '<td>' + hackathonData.judges_checked_in + '</td>' +
                '</tr>' +
                '<tr>' +
                    '<th>Organizers</th>' +
                    '<td>' + hackathonData.organizers_registered + '</td>' +
                    '<td>' + hackathonData.organizers_approved + '</td>' +
                    '<td>' + hackathonData.organizers_checked_in + '</td>' +
                '</tr>' +
            '</tbody>'
        );
    }

    function initAccountSection(accountData) {
        var form = $('#account form');
        form.find('input[name="email"]').val(accountData.email);
        form.find('input[name="first_name"]').val(accountData.first_name);
        form.find('input[name="last_name"]').val(accountData.last_name);
        form.find('input[name="phone"]').val(accountData.phone_number);
        form.find('select[name="shirt_size"]').val(accountData.shirt_size);
        form.find('input[name="github"]').val(accountData.github);
        form.find('input[name="linkedin"]').val(accountData.linkedin);
        form.find('textarea[name="diet"]').val(accountData.diet);
    }

    function initHackerSection(hackerData) {
        var hackerSection = $('#hacker');
        var form = hackerSection.children('form');


        hackerSection.children('h3').text(hackerData.approved? 'Approved' : 'Pending Approval');

        form.find('input[name="school"]').val(hackerData.school);
        form.find('select[name="year"]').val(hackerData.school_year);
        form.find('input[name="major"]').val(hackerData.school_major);
        form.find('textarea[name="interests"]').val(hackerData.interests);

        form.find('#first-hack-true').prop('checked', hackerData.is_first_hackathon);
        form.find('#first-hack-false').prop('checked', !hackerData.is_first_hackathon);

        form.find('#yes_adult').prop('checked', hackerData.is_adult);
        form.find('#no_adult').prop('checked', !hackerData.is_adult);

        if (hackerData.resume_url) {
            form.find('#hacker-resume').text('Download').wrap(
                '<a target="_blank" href="' + hackerData.resume_url + '"></a>');
        } else {
            form.find('#hacker-resume').text('None');
        }

        hackerSection.toggle(true);
    }

    function init(pData) {
        $.ajaxGet({
            url: '/api/hackathon/get/stats',
            success: function (data) {
                initHackathonSection(data, pData.groups, pData.rsvp_confirmed);
            }
        });

        initActionButtons(pData.groups, pData.rsvp_confirmed);

        initAccountSection(pData);

        if (pData.groups.includes(GROUP.hacker) ||
            pData.groups.includes(GROUP.pending_hacker)) {
            $.ajaxGet({
                url: '/api/hacker/get/profile',
                success: function(data) {
                    initHackerSection(data);
                }
            });
        }

    }

    $.ajaxGet({
        url: '/api/user/get/profile',
        success: function(data) {
            init(data);
        }
    });

})(jQuery);
