(function($) {
    'use strict';

    var form = $('form#rsvp');
    var submitBtn = $('button[type="submit"]');
    var yesIcon = 'fa-smile-o';
    var noIcon = 'fa-frown-o';

    // Make emotes visible in submit button
    $('input[name="rsvp"]').change(function() {
        var self = $(this);
        var icons;
        var isYes;

        if (self.is(':checked')) {
            isYes = self.is('#rsvp_yes');
            icons = submitBtn.find('span');
            icons.addClass(isYes? yesIcon : noIcon);
            icons.removeClass(isYes? noIcon : yesIcon);
            icons.css('visibility', 'visible');
        }
    });

    form.ajaxForm({
        url: '/api/attendee/rsvp',
        getData: function() {
            return {
                rsvp_answer: form.find('input[name="rsvp"]').val(),
                extra_info: form.find('textarea[name="extra_info"]').val().trim()
            };
        },
        onAjaxComplete: function() {
            window.location.href = '/user/profile';
        }
    });

})(jQuery);
