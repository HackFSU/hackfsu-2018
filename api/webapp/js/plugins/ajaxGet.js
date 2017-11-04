/**
 * Ajax GET request wrapper with correct headers and using promises
 */

(function($) {

    var defaultAjaxSettings = {
        type: 'GET',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        error: function(response) {
            console.error('Server Error:', response);
            var err = JSON.parse(response.responseText);
            alert(err.cause + ': ' + err.message);
        }
    };

    $.ajaxGet = function(options) {
        var o = $.extend({}, defaultAjaxSettings, options);

        return $.ajax(o);
    };
})(jQuery);