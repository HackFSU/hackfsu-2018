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

    schoolInput.schoolAutocomplete();

    studentType.change(function() {
        var type = studentType.val();
        if (type === 'highschool') {
            studentYear.prop('required', false);
            studentMajor.prop('required', false);
            $('#year').toggle(false);
            $('#major').toggle(false);
        }
        else if (type === 'graduated')  {
            studentYear.prop('required', false);
            studentMajor.prop('required', true);
            $('#year').toggle(false);
            $('#major').toggle(true);
        }
        else {
            studentYear.prop('required', true);
            studentMajor.prop('required', true);
            $('#year').toggle(true);
            $('#major').toggle(true);
        }
    });

    function getInterests() {
        var typeList = [];
        $('input.project-type:checked').each(function () {
            typeList.push($(this).data('value'));
        });
        return typeList.join('; ') + projectTypes.val().trim();
    }

    form.ajaxForm({
        url: '/api/hacker/register',
        useFormData: true,
        getData: function() {
            var hsStudent = studentType.val() === 'highschool';

            var data =  {
                is_first_hackathon: first_hackathon.val() === 'true',
                is_adult: isAdult.val() === 'true',
                is_high_school: hsStudent,
                school_year: hsStudent ? 'HS' : studentYear.val(),
                school_major: hsStudent ? 'N/A' : studentMajor.val().trim(),
                interests: getInterests(),
                resume: resumeField[0].files[0]
            };

            var school_name = schoolInput.val().trim();
            data.school_id = schoolInput.schoolAutocomplete('getId', school_name);
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
