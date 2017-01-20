/**
 * User registration
 */

(function($) {
    'use strict';

    var form = $('form#register_user');
    var firstName = form.find('input[name="first_name"]');
    var lastName = form.find('input[name="last_name"]');
    var emailInput = form.find('input[name="email"]');
    var passwordInput = form.find('input[name="password"]');
    var phoneNumber = form.find('input[name="phone"]');
    var githubLink = form.find('input[name="github"]');
    var linkedInProfile = form.find('input[name="linkedin"]');
    var dietInput = form.find('input[name="diet"]');
    var shirtSize = form.find('input[name="shirt_size"]');
    var mlhCoc = form.find('input[name="mlhcoc"]');
    var mlhDataSharing = form.find('input[name="mlhcoc"]');
    var recaptchaResponse = window.grecaptcha.getResponse();

    /*$('#test button').click(function() {
        console.log('Captcha response?');
        var response = window.grecaptcha.getResponse();
        console.log(response);
        $('#recaptcha-validate').val(response);
    });*/

    form.ajaxForm({
        url: '/api/user/register',
        getData: function() {
            return {
                agree_to_mlh_coc: mlhCoc.val().trim(),
                agree_to_mlh_data_sharing: mlhDataSharing.val().trim(),
                g_recaptcha_response: recaptchaResponse.val().trim(),
                first_name: firstName.val().trim(),
                last_name: lastName.val().trim(),
                email: emailInput.val().trim(),
                password: passwordInput.val().trim(),
                shirt_size: shirtSize.val().trim(),
                phone_number: phoneNumber.val().trim(),
                github: githubLink.val().trim(),
                linkedin: linkedInProfile.val().trim(),
                diet: dietInput.val().trim()
            };
        },
        setDisabled: function(value) {
            firstName.prop('disabled', value);
            lastName.prop('disabled', value);
            emailInput.prop('disabled', value);
            passwordInput.prop('disabled', value);
            phoneNumber.prop('disabled', value);
            githubLink.prop('disabled', value);
            linkedInProfile.prop('disabled', value);
            dietInput.prop('disabled', value);
            shirtSize.prop('disabled', value);
            mlhCoc.prop('disabled', value);
            mlhDataSharing.prop('disabled', value);
            recaptchaResponse.prop('disabled', value);
            emailInput.prop('disabled', value);
            passwordInput.prop('disabled', value);
        },
        onAjaxComplete: function(response) {
            console.log('TODO complete', response);
            // window.location.href = '/user/profile';
        }
    });

})(jQuery);
