(function($) {
    'use strict';

    var GROUP = {
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

        // if (pData.groups.includes(GROUP.hacker)
        // || pData.groups.includes(GROUP.pending_hacker)) {
        //     $.ajaxGet({
        //         url: '/api/hacker/get/profile',
        //         success: function(data) {
        //             initHackerSection(data);
        //         }
        //     });
        // }
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
        var form = $('form#account');
        form.find('input[name="email"]').val(accountData.email);
        form.find('input[name="first_name"]').val(accountData.first_name);
        form.find('input[name="last_name"]').val(accountData.last_name);
        form.find('input[name="phone"]').val(accountData.phone_number);
        form.find('select[name="shirt_size"]').val(accountData.shirt_size);
        form.find('input[name="github"]').val(accountData.github);
        form.find('input[name="linkedin"]').val(accountData.linkedin);
        form.find('input[name="diet"]').val(accountData.diet);
    }

    function initHackerSection(hackerData) {
        // TODO
    }

})(jQuery);
