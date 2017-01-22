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
    var dietInput = form.find('textarea[name="diet"]');
    var shirtSize = form.find('select[name="shirt_size"]');
    var mlhCoc = form.find('input[name="mlhcoc"]');
    var mlhDataSharing = form.find('input[name="mlhcoc"]');

    var dietString = "";
    var dietText = false;

    $('.diet-detail:checkbox').change(function() {
        dietString = "";
        dietText = false;
        if ($('#vegetarian').prop('checked')) {
            dietString += "Vegetarian, ";
        }
        if ($('#vegan').prop('checked')) {
            dietString += "Vegan, ";
        }
        if ($('#allergy').prop('checked')) {
            dietString += "Allergy, ";
            dietText = true;
        }
        if ($('#diet-other').prop('checked')) {
            dietString += "Other, ";
            dietText = true;
        }
        if (dietText)
            $('#dietbox').fadeIn();
        else
            $('#dietbox').fadeOut();
    });

    form.ajaxForm({
        url: '/api/user/register',
        getData: function() {
            return {
                agree_to_mlh_coc: mlhCoc.val().trim(),
                agree_to_mlh_data_sharing: mlhDataSharing.val().trim(),
                g_recaptcha_response: 'TODO',//window.grecaptcha.getResponse(),
                first_name: firstName.val().trim(),
                last_name: lastName.val().trim(),
                email: emailInput.val().trim(),
                password: passwordInput.val().trim(),
                shirt_size: shirtSize.val().trim(),
                phone_number: phoneNumber.val().trim().replace(/\D/g,''),
                github: githubLink.val().trim(),
                linkedin: linkedInProfile.val().trim(),
                diet: dietText ? dietString + dietInput.val().trim() : dietString
            };
        },
        setDisabled: function(value) {
            console.log(dietString);
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
            emailInput.prop('disabled', value);
            passwordInput.prop('disabled', value);
        },
        onAjaxComplete: function(response) {
            console.log('TODO complete', response);
            window.location.href = '/registration/hacker';
        }
    });

})(jQuery);
