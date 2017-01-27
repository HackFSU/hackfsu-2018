(function($) {
    'use strict';

    var GROUP = {
        attendee: 'attendee',
        hacker: 'hacker',
        judge: 'judge',
        mentor: 'mentor',
        organizer: 'organizer',
        pending_hacker: 'pending-hacker',
        pending_judge: 'pending-judge',
        pending_mentor: 'pending-mentor',
        pending_organizer: 'pending-organizer'
    };

    var hackerBtn = $('#hackerBtn');
    var mentorBtn = $('#mentorBtn');
    var judgeBtn = $('#judgeBtn');
    var organizerBtn = $('#organizerBtn');

    $.ajaxGet({
        url: '/api/user/get/profile',
        success: function(data) {
            init(data);
        }
    });

    function init(pData) {
        initActionButtons(pData.groups);
        initAccountSection(pData);

        if (pData.groups.includes(GROUP.hacker)
        || pData.groups.includes(GROUP.pending_hacker)) {
            $.ajaxGet({
                url: '/api/hacker/get/profile',
                success: function(data) {
                    initHackerSection(data);
                }
            });
        }
    }

    function initActionButtons(groups) {
        if (!groups.includes(GROUP.hacker)
        && !groups.includes(GROUP.pending_hacker)) {
            hackerBtn.prop('disabled', false);
            hackerBtn.prop('title', 'Go to Hacker Registration');
            hackerBtn.click(function() {
                window.location.href = '/registration/hacker'
            })
        }
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

})(jQuery);
