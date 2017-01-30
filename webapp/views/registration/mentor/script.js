/**
 * User registration
 */

(function($) {
    'use strict';

    var form = $('form#register');
    var affiliationInput = form.find('input[name="school"]');
    var motivationInput = form.find('textarea[name="school"]');
    var projectTypes = form.find('textarea[name="project-types"]');

    function getAvailability() {
        var avail = 0;
        $('input.availability:checked').each(function () {
            avail += $(this).data('value');
        });
        return avail;
    }

    function getSkills() {
        var skills = [];
        $('input.project-type:checked').each(function () {
            skills.push($(this).data('value'));
        });
        skills.push(projectTypes.val().trim());
        return '' + skills.join('; ');
    }

    form.ajaxForm({
        url: '/api/mentor/register',
        getData: function() {
            var data = {
                affiliation: form.find('input[name="affiliation"]').val().trim(),
                skills: getSkills(),
                motivation: form.find('textarea[name="motivation"]').val().trim(),
                availability: getAvailability()
            };

            if (data.availability === 0) {
                alert('You must select at least one time you think you can help.');
                throw new Error(JSON.stringify(data));
            }

            return data;
        },
        onAjaxComplete: function() {
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
