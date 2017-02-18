/**
 * Help request submission
 */

(function($) {
    'use strict';

    var form = $('form#help');
    var locationFloor = form.find('select[name="location_floor"]');
    var requestDetails = form.find('textarea[name="request_details"]');
    var floorMap = $('#floor-map');
    var mapImage = floorMap.find('img');
    var mapPin = floorMap.find('.map-pin');

    locationFloor.change(function() {
        var imgSrc = $(this).find('option:selected').data('img');
        mapImage.attr('src', imgSrc);
        mapPin.toggle(false);
    });

    function positionPin() {
        if (!mapPin.is(':visible')) {
            return;
        }

        var x = mapPin.data('x-percent')/10000*mapImage.innerWidth();
        var y = mapPin.data('y-percent')/10000*mapImage.innerHeight();
        mapPin.css('left', x + 'px');
        mapPin.css('top', y + 'px');
    }

    $(window).resize(function() {
        positionPin();
    });

    mapImage.on('dragstart', function(ev) {
        ev.preventDefault();
    });
    mapImage.click(function(ev) {
        var offset = $(this).offset();
        var x = Math.round(ev.pageX - offset.left);
        var y = Math.round(ev.pageY - offset.top);

        mapPin.toggle(true);
        mapPin.data('x-percent', Math.round(x/mapImage.innerWidth()*10000.0));
        mapPin.data('y-percent', Math.round(y/mapImage.innerHeight()*10000.0));
        positionPin();
    });

    function getRequest() {
        var requestItems = [];
        $('input.request-topic:checked').each(function () {
            requestItems.push($(this).data('value'));
        });
        requestItems.push(requestDetails.val().trim());
        return '' + requestItems.join('; ');
    }

    form.ajaxForm({
        url: '/api/mentor/request/create',
        useFormData: true,
        getData: function() {
            if (!mapPin.is(':visible')) {
                alert('Please click on your location in the map');
                throw new Error('Map location required.');
            }

            var data = {
                request: getRequest(),
                g_recaptcha_response: window.grecaptcha.getResponse(),
                location_floor: locationFloor.val(),
                location_x: mapPin.data('x-percent'),
                location_y: mapPin.data('y-percent'),
                attendee_name: $('input[name="attendee_name"]').val().trim(),
                attendee_description: $('input[name="attendee_description"]').val().trim(),
                attendee_phone: $('input[name="attendee_phone"]').val().trim().replace(/[\D]/g, '')
            };

            console.log(data);

            if (!data.g_recaptcha_response) {
                alert('Captcha required.');
                throw new Error('Captcha required.');
            }

            return data;
        },
        onAjaxComplete: function() {
            alert('Help Request Submitted! If no one comes to you in 10 minutes, go to the mentor lounge.');
            window.location.href = '/';
        },
        afterError: function() {
            window.grecaptcha.reset();
        }
    });

})(jQuery);
