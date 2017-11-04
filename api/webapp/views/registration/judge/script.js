/**
 * Judge registration
 */

(function($) {
    'use strict';

    var form = $('form#register');

    form.ajaxForm({
        url: '/api/judge/register',
        getData: function() {
            return {
                affiliation: form.find('input[name="affiliation"]').val().trim(),
                organizer_contact: form.find('input[name="organizer_contact"]').val().trim()
            };
        },
        onAjaxComplete: function() {
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
