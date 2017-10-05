(function($) {
    'use strict';

    var form = $('form#completeReset');

    form.ajaxForm({
        url: '/api/user/password/reset/complete',
        getData: function() {
            return {
                new_password: $('input[name="password"]').val()
            };
        },
        onAjaxComplete: function() {
            window.location.href = '/user/login';
        }
    });

})(jQuery);
