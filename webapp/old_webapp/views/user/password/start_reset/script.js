(function($) {
    'use strict';

    var form = $('form#startReset');

    form.ajaxForm({
        url: '/api/user/password/reset/start',
        getData: function() {
            var data = {
                g_recaptcha_response: window.grecaptcha.getResponse(),
                email: $('input[name="email"]').val().trim()
            };

            if (!data.g_recaptcha_response) {
                alert('Captcha required.');
                throw new Error('Captcha required.');
            }
            return data;
        },
        onAjaxComplete: function() {
            alert('An email will been sent to the given address if the account exists.');
            window.location.href = '/user/login';
        },
        afterError: function() {
            window.grecaptcha.reset();
        }
    });

})(jQuery);
