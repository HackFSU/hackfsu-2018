(function($) {
    'use strict';

    var GROUP = {
        user: 'user',
        attendee: 'attendee',
        hacker: 'hacker',
        judge: 'judge',
        mentor: 'mentor',
        organizer: 'organizer',
        pending_hacker: 'pending-hacker',
        pending_judge: 'pending-judge',
        pending_mentor: 'pending-mentor',
        pending_organizer: 'pending-organizer',
        admin: 'admin'
    };

    function initActionButtons(groups) {
        var buttonContainer = $('#action-buttons');
        var buttons = [];
        var i, btn;

        if (!groups.includes(GROUP.hacker) &&
            !groups.includes(GROUP.pending_hacker)) {

            if (!groups.includes(GROUP.organizer) &&
                !groups.includes(GROUP.pending_organizer) &&
                !groups.includes(GROUP.judge) &&
                !groups.includes(GROUP.pending_judge)) {

                buttons.push({
                    'text': 'Register as a hacker',
                    'url': '/registration/hacker'
                });
            }



            if (!groups.includes(GROUP.mentor) &&
                !groups.includes(GROUP.pending_mentor)) {

                buttons.push({
                    'text': 'Register as a mentor',
                    'url': '/registration/mentor'
                });
            }

            if (!groups.includes(GROUP.judge) &&
                !groups.includes(GROUP.pending_judge)) {

                buttons.push({
                    'text': 'Register as a judge',
                    'url': '/registration/judge'
                });
            }

            if (!groups.includes(GROUP.organizer) &&
                !groups.includes(GROUP.pending_organizer)) {

                buttons.push({
                    'text': 'Register as a organizer',
                    'url': '/registration/organizer',
                    'title': 'Coming soon',
                    'disabled': true
                });
            }
        } else if (!groups.includes(GROUP.mentor) &&
            !groups.includes(GROUP.pending_mentor)) {

            buttons.push({
                'text': 'Register as a mentor',
                'url': '/registration/mentor'
            });
        }

        if (groups.includes(GROUP.organizer)) {
            buttons.push({
                'text': 'Django Admin Panel',
                'url': '/admin/django'
            });
        }

        var onClick = function() {
            window.location.href = $(this).data('url');
        };

        for (i = 0; i < buttons.length; ++i) {
            btn = $('<button class="btn btn-form"></button>');
            btn.prop('title', buttons[i].title);
            btn.prop('disabled', !!buttons[i].disabled);
            btn.data('url', buttons[i].url);
            btn.text(buttons[i].text);

            btn.appendTo(buttonContainer);
            btn.click(onClick);
        }
    }

    function initHackathonSection(hackathonData, groups) {
        var section = $('#hackathon');
        var start = moment(hackathonData.hackathon_start, 'YYYY-MM-DD');
        var end = moment(hackathonData.hackathon_end, 'YYYY-MM-DD');

        groups = [].concat(groups);
        var i = groups.indexOf(GROUP.attendee);
        if (i !== -1) {
            groups.splice(i, 1);
        }

        if (groups.length === 0) {
            groups.push('regular ' + GROUP.user);
        }

        var groupString = 'You are a ' + groups.sort().join(' and a ');
        groupString = groupString.replace(/-/g, ' ').replace(/(a)\s([aeio])/g, 'an $2') + '.';

        // Account for not allowed data (-1)
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
        initActionButtons(pData.groups);

        $.ajaxGet({
            url: '/api/hackathon/get/stats',
            success: function (data) {
                initHackathonSection(data, pData.groups);
            }
        });

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
