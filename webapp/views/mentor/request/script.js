/**
 * Help request submission
 */

(function($) {
    'use strict';

    var form = $('form#help');
    var locationFloor = form.find('select[name="location_floor"]');
    var floorMap = $('#floor-map');
    var mapImage = floorMap.find('img');
    var mapPin = floorMap.find('.map-pin');
    var submitBtn = form.find('button[type="submit"]');


    function positionPin() {
        if (!mapPin.is(':visible')) {
            return;
        }

        var x = mapPin.data('x-percent')/10000.0*mapImage.innerWidth();
        var y = mapPin.data('y-percent')/10000.0*mapImage.innerHeight();
        mapPin.css('left', x + 'px');
        mapPin.css('top', y + 'px');
    }

    $(window).resize(function() {
        positionPin();
    });

    mapImage.on('dragstart', function(ev) {
        ev.preventDefault();
    });

    var pathArray = window.location.pathname.split('/');
    var requestId = pathArray[pathArray.length - 2];

    function submitClaim() {
        submitBtn.prop('disabled', true);
        window.hackUtil.ajaxJsonSubmit({
            url: '/api/mentor/request/claim',
            data: JSON.stringify({
                    help_request_id: submitBtn.data('id')
            })
        }).done(function() {
            alert('You have successfully claimed this request');
        }).fail(function() {
            submitBtn.prop('disabled', false);
        });
    }

    function releaseClaim() {
        submitBtn.prop('disabled', true);
        window.hackUtil.ajaxJsonSubmit({
            url: '/api/mentor/request/release_claim',
            data: JSON.stringify({
                    help_request_id: submitBtn.data('id')
            })
        }).done(function() {
            alert('You have successfully released your claim of this request');
            window.location.href = '/mentor';
        }).fail(function() {
            submitBtn.prop('disabled', false);
        });
    }

    $.ajaxGet({
        url: '/api/mentor/request/get/id/' + requestId,
        success: function (res) {
            var hr = res['help_request'];

            console.log(hr);
            form.find('input[name="attendee_name"]').val(hr.attendee.name);
            form.find('input[name="attendee_description"]').val(hr.attendee.description);
            form.find('textarea[name="request"]').val(hr.request);
            locationFloor.val(hr.location.floor);
            mapImage.attr('src', locationFloor.find('option:selected').data('img'));

            mapPin.data('x-percent', hr.location.x);
            mapPin.data('y-percent', hr.location.y);
            mapPin.toggle(true);
            positionPin();

            submitBtn.data('id', hr.id);
            if (hr.assigned_mentor && hr.assigned_mentor.is_me) {
                submitBtn.text('Release Claim');
                form.submit(function(ev) {
                    ev.preventDefault();
                    releaseClaim();
                });
            } else {
                submitBtn.text('Claim');
                form.submit(function(ev) {
                    ev.preventDefault();
                    submitClaim();
                });
            }
            submitBtn.toggle(true);
        }
    });

})(jQuery);
