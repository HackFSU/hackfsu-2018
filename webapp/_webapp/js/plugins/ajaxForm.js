/**
 * $form.ajaxForm(options)
 *
 * A generic way to make quick ajax forms which check for validation using the
 * parsley form validation framework.
 *
 * Data is sent as JSON to the server.
 *
 * Need to send files? Set useFormData to true to convert the data to a formData object and send multipart/formdata
 */

(function($) {
    'use strict';

    var defaultOptions = {
        url: '',
        useFormData: false,
        getData: function() { return {}; },
        setDisabled: function(value, form) {
            form.find('input, textarea, select, button').prop('disabled', value);
        },
        onAjaxComplete: function(response, data) { console.log(response, data); },
        onAjaxError: function(error, data) { console.error(error); },
        afterError: function() {},
        parsleyOptions: {}
    };

    function fillValuesFromUrlParams(form) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            param, name, value, field, i;

        for (i = 0; i < sURLVariables.length; i++) {
            param = sURLVariables[i].split('=');

            if (param.length === 2) {
                name = param[0].replace('"','');
                value = param[1];
                field = form.find('[name="' + name + '"]');
                if (field.length === 1 && field.is('input, select, textarea')) {
                    field.val(value);
                }
            }
        }
    }

    $.fn.ajaxForm = function(options) {
        if (!this.is('form')) {
            throw TypeError('Must be a form element');
        }
        var self = $(this);
        var o = $.extend({}, defaultOptions, options);
        var parsleyFormInstance = this.parsley(o.parsleyOptions);
        var canSubmit = true;

        fillValuesFromUrlParams(self);

        this.on('submit', function(ev) {
            ev.preventDefault();
            if (!canSubmit) {
                return;
            }
            canSubmit = false;
            o.setDisabled(true, self);

            parsleyFormInstance.whenValidate()
            .done(function() {
                var jsonData;
                var ajaxOptions = {
                    url: o.url
                };

                try {
                    jsonData = o.getData();
                } catch (err) {
                    console.error('Unable to retrieve data: ', err);
                    canSubmit = true;
                    o.setDisabled(false, self);
                    o.onAjaxError(err, {});
                    o.afterError();
                    return;
                }

                if (o.useFormData) {
                    // Send formData
                    ajaxOptions.data = window.hackUtil.jsonToFormData(jsonData);
                    ajaxOptions.processData = false;
                    ajaxOptions.contentType = false;
                } else {
                    // Send JSON
                    ajaxOptions.data = JSON.stringify(jsonData);
                }

                window.hackUtil.ajaxJsonSubmit(ajaxOptions)
                .done(function(response) {
                    o.onAjaxComplete(response, jsonData);
                })
                .fail(function(error) {
                    canSubmit = true;
                    o.setDisabled(false, self);
                    o.onAjaxError(error, jsonData);
                    o.afterError();
                });
            });

        });

        /**
         * Custom UI Updates
         * TODO
         */

        parsleyFormInstance.on('form:error', function(parsleyForm) {
            // console.error('parsley:form:error', parsleyForm);
        });

        parsleyFormInstance.on('form:success', function(parsleyForm) {
            // console.log('parsley:form:success', parsleyForm);
        });

        parsleyFormInstance.on('field:error', function(parsleyField) {
            // console.error('parsley:field:error', parsleyField);
        });

        parsleyFormInstance.on('field:success', function(parsleyField) {
            // console.log('parsley:field:success', parsleyField);
        });

        return parsleyFormInstance;
    };

})(jQuery);
