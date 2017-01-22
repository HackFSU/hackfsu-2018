/**
 * User registration
 */

(function($) {
    'use strict';

    var form = $('form#register_hacker');
    var studentType = form.find('select[name="student_type"]');
    var schoolInput = form.find('input[name="school"]');
    var schoolCode = form.find('input[name="school_code"]');
    var studentYear = form.find('select[name="year"]');
    var studentMajor = form.find('input[name="major"]');
    var first_hackathon = form.find('input[name="first_hackathon"]');
    var projectTypes = form.find('input[name="project-types"]');
    var isAdult = form.find('input[name="over_18"]');
    var jobPref = form.find('input[name="job"]');
    var resumeField = form.find('input[name="resume"]');

    studentType.change(function() {
        console.log(studentType.val());
        if (studentType.val() === 'highschool') {
            studentYear.prop('required', false);
            $('#year').fadeOut();
            studentMajor.prop('required', false);
            $('#major').fadeOut();
        }
        else if (studentType.val() === 'graduated')  {
            studentYear.prop('required', false);
            $('#year').fadeOut();
        }
        else {
            studentYear.prop('required', true);
            studentMajor.prop('required', true);
            $('#year').fadeIn();
            $('#major').fadeIn();
        }
    });

    var projectTypesString = "";

    $('.project-type:checkbox').change(function() {
        projectTypesString = "";
        if ($('#frontend').prop('checked')) {
            projectTypesString += "Frontend, ";
        }
        if ($('#backend').prop('checked')) {
            projectTypesString += "Backend, ";
        }
        if ($('#web').prop('checked')) {
            projectTypesString += "Web, ";
        }
        if ($('#hardware').prop('checked')) {
            projectTypesString += "Hardware, ";
        }
        if ($('#ios').prop('checked')) {
            projectTypesString += "iOS, ";
        }
        if ($('#android').prop('checked')) {
            projectTypesString += "Android, ";
        }
    });

    form.ajaxForm({
        url: '/api/user/register',
        getData: function() {
            return {
                is_first_hackathon: first_hackathon.val().trim(),
                is_adult: isAdult.val().trim(),
                is_high_school: studentType === 'highschool' ? true : false,
                school_year: studentType === 'highschool' ? '' : studentYear.val().trim(),
                school_major: studentType === 'highschool' ? '' : studentMajor.val().trim(),
                school_id: schoolCode.val().trim(),
                new_school_name: school_code >= 0 ? '' : schoolInput.val().trim()

            };
        },
        setDisabled: function(value) {
            console.log(projectTypesString);
            studentType.prop('disabled', value);
            schoolInput.prop('disabled', value);
            studentYear.prop('disabled', value);
            studentMajor.prop('disabled', value);
            first_hackathon.prop('disabled', value);
            projectTypes.prop('disabled', value);
            jobPref.prop('disabled', value);
            resumeField.prop('disabled', value);
        },
        onAjaxComplete: function(response) {
            console.log('TODO complete', response);
            // window.location.href = '/user/profile';
        }
    });

})(jQuery);
