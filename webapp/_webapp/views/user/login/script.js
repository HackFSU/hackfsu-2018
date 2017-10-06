/**
 * User login
 */

(function($) {
    'use strict';

    var form = $('form#login');
    var emailInput = form.find('input[name="email"]');
    var passwordInput = form.find('input[name="password"]');

    form.ajaxForm({
        url: '/api/user/login',
        getData: function() {
            return {
                email: emailInput.val().trim(),
                password: passwordInput.val()
            };
        },
        onAjaxComplete: function(response) {
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
