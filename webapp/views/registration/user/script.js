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
        if (dietText) {
            $('#dietbox').toggle(true);
        } else {
            $('#dietbox').toggle(false);
        }
    });

    function getDiet() {
        var diets = [];
        $('input.diet-detail:checked').each(function () {
            diets.push(value);
        });
        if ($('#diet-other').is(':checked')) {
            diets.push(dietInput.val().trim());
        }
        return '' + diets.join('; ');
    }

    form.ajaxForm({
        url: '/api/user/register',
        getData: function() {
            return {
                agree_to_mlh_coc: mlhCoc.is(':checked'),
                agree_to_mlh_data_sharing: mlhtcpp.is(':checked'),
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
        onAjaxComplete: function(response) {
            console.log('TODO complete', response);
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
