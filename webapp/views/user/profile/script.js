(function($) {
    'use strict';
    // Get profile data

    $.get({
        url: '/api/user/get/profile',
        success: function(data) {
            console.log('profile', data);
        },
        error: function(err) {
            console.error(err);
        }
    });
})(jQuery);
