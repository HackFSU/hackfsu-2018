(function() {
    'use strict';

    /**
     * Subscribe form
     * TODO
     */
    var form = $('form#subscribe');
    var submitBtn = form.find('button[type="submit"]');

    form.ajaxForm({
        url: '/api/hackathon/subscribe',
        getData: function() {
            var data = {
                email: form.find('input[name="email"]').val().trim()
            };
            return data;
        },
        setDisabled: function(value) {
            submitBtn.prop('disabled', value);
        },
        onAjaxComplete: function(data) {
            // TODO
            alert('Succesfully subscribed ' + data.email);
        },
        onAjaxError: function(data, error) {
            // TODO
            console.log('data', data);
            alert(error);
        }
    });
})();
