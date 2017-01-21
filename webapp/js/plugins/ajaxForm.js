/**
 * $form.ajaxForm(options)
 *
 * A generic way to make quick ajax forms which check for validation using the
 * parsley form validation framework.
 *
 * Data is sent as JSON to the server.
 */

(function($) {
    'use strict';

    var defaultOptions = {
        url: '',
        getData: function() { return {}; },
        setDisabled: function(value) { return value; },
        onAjaxComplete: function(data, response) { console.log(response); },
        onAjaxError: function(data, error) { console.error(error); },
        parsleyOptions: {}
    };

    function ajaxJsonSubmit(url, data) {
        var dfd = $.Deferred();
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            headers: {
                'HTTP_X_CSRFTOKEN': Cookies.get('csrftoken')
            },
            data: JSON.stringify(data),
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
                dfd.reject(response);
            }
        });
        return dfd.promise();
    }

    $.fn.ajaxForm = function(options) {
        if (!this.is('form')) {
            throw TypeError('Must be a form element');
        }

        var o = $.extend({}, defaultOptions, options);
        var parsleyFormInstance = this.parsley(o.parsleyOptions);
        var canSubmit = true;

        this.on('submit', function(ev) {
            ev.preventDefault();
            if (!canSubmit) {
                return;
            }
            canSubmit = false;
            o.setDisabled(true);

            parsleyFormInstance.whenValidate()
            .done(function() {
                var data = o.getData();
                ajaxJsonSubmit(o.url, data)
                .done(function(response) {
                    o.onAjaxComplete(response, data);
                })
                .fail(function(error) {
                    canSubmit = true;
                    o.setDisabled(false);
                    o.onAjaxError(error, data);
                });
            });

        });

        /**
         * Custom UI Updates
         * TODO
         */

        parsleyFormInstance.on('form:error', function(parsleyForm) {
            console.error('parsley:form:error', parsleyForm);
        });

        parsleyFormInstance.on('form:success', function(parsleyForm) {
            // console.log('parsley:form:success', parsleyForm);
        });

        parsleyFormInstance.on('field:error', function(parsleyField) {
            console.error('parsley:field:error', parsleyField);
        });

        parsleyFormInstance.on('field:success', function(parsleyField) {
            // console.log('parsley:field:success', parsleyField);
        });

        return parsleyFormInstance;
    };

})(jQuery);
