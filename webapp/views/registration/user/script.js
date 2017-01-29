/**
 * User registration
 */

(function($) {
    'use strict';

    var form = $('form#register_user');
    var attendeeType = form.find('select[name="attendee_type"]');
    var firstName = form.find('input[name="first_name"]');
    var lastName = form.find('input[name="last_name"]');
    var emailInput = form.find('input[name="email"]');
    var passwordInput = form.find('input[name="password"]');
    var phoneNumber = form.find('input[name="phone"]');
    var githubLink = form.find('input[name="github"]');
    var linkedInProfile = form.find('input[name="linkedin"]');
    var dietInput = form.find('textarea[name="diet"]');
    var shirtSize = form.find('select[name="shirt_size"]');
    var mlhCoc = form.find('input[name="mlhcoc"]');
    var mlhTac = form.find('input[name="mlhtac"]');



    $('#diet-detail, #allergy').change(function () {
        dietInput.toggle($('#diet-other').is(':checked') || $('#allergy').is(':checked'));
    });

    function getDiet() {
        var diets = [];
        $('input.diet-detail:checked').each(function () {
            diets.push($(this).data('value'));
        });
        if ($('#diet-other').is(':checked') || $('#allergy').is(':checked')) {
            diets.push(dietInput.val().trim());
        }
        return '' + diets.join('; ');
    }

    form.ajaxForm({
        url: '/api/user/register',
        getData: function() {
            return {
                agree_to_mlh_coc: mlhCoc.is(':checked'),
                agree_to_mlh_data_sharing: mlhTac.is(':checked'),
                g_recaptcha_response: window.grecaptcha.getResponse(),
                first_name: firstName.val().trim(),
                last_name: lastName.val().trim(),
                email: emailInput.val().trim(),
                password: passwordInput.val(),
                shirt_size: shirtSize.val().trim(),
                phone_number: phoneNumber.val().trim().replace(/\D/g,''),
                github: githubLink.val().trim(),
                linkedin: linkedInProfile.val().trim(),
                diet: getDiet()
            };
        },
        onAjaxComplete: function() {
            var destination = '/user/profile';
            var type = attendeeType.val();
            if (type !== 'other') {
                destination = '/registration/' + type;
            }

            window.location.href = destination;
        },
        afterError: function() {
            window.grecaptcha.reset();
        }
    });

})(jQuery);
