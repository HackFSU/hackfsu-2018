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
        setDisabled: function(value) { return value; },
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

    function ajaxJsonSubmit(options) {
        var dfd = $.Deferred();
        var defaultAjaxOptions = {
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            success: function(response) {
                if (response.error) {
                    console.error('Server Error:', response.error);
                    dfd.reject(response.error);
                } else {
                    dfd.resolve(response);
                }
            },
            error: function(response) {
                console.error('Server Error:', response);
                var err = JSON.parse(response.responseText);
                alert(err.cause + ': ' + err.message);
                dfd.reject(response);
            }
        };

        $.ajax($.extend({}, defaultAjaxOptions, options));

        return dfd.promise();
    }

    function jsonToFormData(jsonData) {
        var fd = new FormData();
        for (var key in jsonData) {
            if (jsonData.hasOwnProperty(key) && jsonData[key] !== null && jsonData[key] !== undefined) {
                fd.append(key, jsonData[key]);
            }
        }
        return fd;
    }


    $.fn.ajaxForm = function(options) {
        if (!this.is('form')) {
            throw TypeError('Must be a form element');
        }

        var o = $.extend({}, defaultOptions, options);

        if (!o.setDisabled) {
            o.setDisabled = function() {
                self.find('input, textarea, select, button').prop('disabled', value);
            };
        }

        var parsleyFormInstance = this.parsley(o.parsleyOptions);
        var canSubmit = true;
        fillValuesFromUrlParams($(this));

        this.on('submit', function(ev) {
            ev.preventDefault();
            if (!canSubmit) {
                return;
            }
            canSubmit = false;
            o.setDisabled(true);

            parsleyFormInstance.whenValidate()
            .done(function() {
                var jsonData = o.getData();
                var ajaxOptions = {
                    url: o.url
                };

                if (o.useFormData) {
                    // Send formData
                    ajaxOptions.data = jsonToFormData(jsonData);
                    ajaxOptions.processData = false;
                    ajaxOptions.contentType = false;
                } else {
                    // Send JSON
                    ajaxOptions.data = JSON.stringify(jsonData);
                }

                ajaxJsonSubmit(ajaxOptions)
                .done(function(response) {
                    o.onAjaxComplete(response, jsonData);
                })
                .fail(function(error) {
                    canSubmit = true;
                    o.setDisabled(false);
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
