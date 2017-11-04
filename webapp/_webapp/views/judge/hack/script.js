/**
 * Help request submission
 */

(function($) {
    'use strict';

    var form = $('form#grade');
    var pathArray = window.location.pathname.split('/');
    var assignementId = pathArray[pathArray.length - 2];
    var overallSection = $('#overall');
    var extraSection = $('#extra');
    var btnCancel = $('#cancel');

    function cancelAssignment(btn) {
        btn.prop('disabled', true);
        window.hackUtil.ajaxJsonSubmit({
            url: '/api/judge/assignment/cancel',
            data: JSON.stringify({
                judging_assignment_id: assignementId
            })
        }).done(function() {
            alert('Assignment canceled!');
            window.location.href = '/judge/';
        }).fail(function() {
            btn.prop('disabled', false);
        });
    }

    function submitGrade(btn) {
        btn.prop('disabled', true);
        window.hackUtil.ajaxJsonSubmit({
            url: '/api/mentor/request/claim',
            data: JSON.stringify({
                    help_request_id: submitBtn.data('id')
            })
        }).done(function() {
            alert('You have successfully claimed this request');
            $('#status').text('Claimed by me');
        }).fail(function() {
            btn.prop('disabled', false);
        });
    }


    function addInput(section, criteria) {
        var fieldSet = $(
            '<fieldset class="row">' +
                '<div class="field-label col-md-3">'+criteria.name+' *</div>' +
                '<div class="col-md-9">' +
                    '<p>'+criteria.description_short+'</p>' +
                    '<select class="responsive" name="'+criteria.id+criteria.name+'" data-id="'+criteria.id+'" required>'+
                        '<option value="0" disabled selected></option>' +
                        '<option value="20">1</option>' +
                        '<option value="40">2</option>' +
                        '<option value="60">3</option>' +
                        '<option value="80">4</option>' +
                        '<option value="100">5</option>' +
                    '</select>' +
                '</div>' +
            '</fieldset>'
        );

        section.append(fieldSet);
    }


    $.ajaxGet({
        url: '/api/judge/get/hack_with_criteria?judging_assignment_id=' + assignementId,
        success: function (res) {
            console.log(res);
            $('#table-number').text(res['hack_table_number']);
            $('#hack-name').text(res['hack_name']);
            var overallCrit = res['overall_criteria'];
            var extraCrit = res['extra_criteria'];

            // Setup Sections
            overallCrit.forEach(function(criteria) {
                addInput(overallSection, criteria);
            });

            if (extraCrit.length > 0) {
                extraCrit.forEach(function(criteria) {
                    addInput(extraSection, criteria);
                });
            } else {
                extraSection.append('<p>N/A</p>');
            }


            // Setup Buttons
            btnCancel.click(function() {
                cancelAssignment($(this));
            });

            // Initialize Form
            form.ajaxForm({
                url: '/api/judge/assignment/submit_grades',
                useFormData: true,
                getData: function() {
                    var grades = [];

                    $('select').each(function(i, e) {
                        e = $(e);
                        var grade = [e.data('id'), e.val()];
                        grades.push(grade)
                    });
                    return {
                        judging_assignment_id: assignementId,
                        criteria_grades: grades
                    };
                },
                onAjaxComplete: function() {
                    alert('Hack Judged!');
                    window.location.href = '/judge';
                }
            });

        }
    });

})(jQuery);
