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
    var projectTypes = form.find('textarea[name="project-types"]');
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
        var interests = [];
        $('input.project-type:checked').each(function () {
            interests.push($(this).data('value'));
        });
        interests.push(projectTypes.val().trim());
        return '' + interests.join('; ');
    }

    form.ajaxForm({
        url: '/api/hacker/register',
        useFormData: true,
        getData: function() {
            var hsStudent = studentType.val() === 'highschool';

            var data =  {
                is_first_hackathon: form.find('input[name="first_hackathon"]:checked').val() === 'true',
                is_adult: form.find('input[name="over_18"]:checked').val() === 'true',
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
            form.find('input, textarea, select, button').prop('disabled', value);
        },
        onAjaxComplete: function(response) {
            console.log('TODO complete', response);
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
