(function($) {
    'use strict';

    $('#test button').click(function() {
        console.log('Captcha response?');
        var response = window.grecaptcha.getResponse();
        console.log(response);
        $('#test textarea').val(response);
    });

})(jQuery);
