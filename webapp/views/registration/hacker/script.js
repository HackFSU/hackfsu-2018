/**
 * User registration
 */

(function($) {
    'use strict';

    var form = $('form#register_hacker');
    var studentType = form.find('select[name="student_type"]');
    var schoolInput = form.find('input[name="school"]');
    var studentYear = form.find('select[name="year"]');
    var studentMajor = form.find('input[name="major"]');
    var first_hackathon = form.find('input[name="first_hackathon"]');
    var projectTypes = form.find('textarea[name="project-types"]');
    var isAdult = form.find('input[name="over_18"]');
    // var jobPref = form.find('input[name="job"]');
    var resumeField = form.find('input[name="resume"]');

    schoolInput.schoolInput();

    studentType.change(function() {
        if (studentType.val() === 'highschool') {
            studentYear.prop('required', false);
            $('#year').toggle(false);
            studentMajor.prop('required', false);
            $('#major').toggle(false);
        }
        else if (studentType.val() === 'graduated')  {
            studentYear.prop('required', false);
            $('#year').toggle(false);
        }
        else {
            studentYear.prop('required', true);
            studentMajor.prop('required', true);
            $('#year').toggle(true);
            $('#major').toggle(true);
        }
    });

    var projectTypesString = "";

    $('.project-type:checkbox').change(function() {
        projectTypesString = "";
        if ($('#frontend').prop('checked')) {
            projectTypesString += "Front-end, ";
        }
        if ($('#backend').prop('checked')) {
            projectTypesString += "Back-end, ";
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
        if ($('#vr').prop('checked')) {
            projectTypesString += "Virtual Reality, ";
        }
        if ($('#design-hack').prop('checked')) {
            projectTypesString += "Design, ";
        }
    });

    form.ajaxForm({
        url: '/api/hacker/register',
        getData: function() {
            var data =  {
                is_first_hackathon: first_hackathon.val() === 'true',
                is_adult: isAdult.val() === 'true',
                is_high_school: studentType === 'highschool',
                school_year: studentType === 'highschool' ? '' : studentYear.val().trim(),
                school_major: studentType === 'highschool' ? '' : studentMajor.val().trim(),
                interests: projectTypesString + projectTypes.val().trim()
            };

            var school_name = schoolInput.val().trim();
            data.school_id = schoolInput.schoolInput('getId', school_name);
            if (!data.school_id) {
                data.new_school_name = school_name;
            }
            return data;
        },
        setDisabled: function(value) {
            studentType.prop('disabled', value);
            schoolInput.prop('disabled', value);
            studentYear.prop('disabled', value);
            studentMajor.prop('disabled', value);
            first_hackathon.prop('disabled', value);
            projectTypes.prop('disabled', value);
            // jobPref.prop('disabled', value);
            resumeField.prop('disabled', value);
        },
        onAjaxComplete: function(response) {
            console.log('TODO complete', response);
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
