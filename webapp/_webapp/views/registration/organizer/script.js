/**
 * Organizer registration
 */

(function($) {
    'use strict';

    var form = $('form#register');

    form.ajaxForm({
        url: '/api/organizer/register',
        getData: function() {
            return {
                affiliation: form.find('input[name="affiliation"]').val().trim(),
                motivation: form.find('textarea[name="motivation"]').val().trim(),
                agree_to_terms: form.find('#terms').is(':checked'),
                teams: form.find('input[name="teams"]').val().trim()
            };
        },
        onAjaxComplete: function() {
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
