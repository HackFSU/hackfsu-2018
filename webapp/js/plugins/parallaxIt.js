/**
 * $.fn.parallaxIt(options)
 *
 * Slightly moves the background on page scroll, making a dynamic paralax
 * effect.
 *
 * It is best to start with the following CSS for speed reasons.
 *      background-position: 50% 0%;
 */

(function($) {
    'use strict';

    var defaultOptions = {
        speed: 0.2
    };

    $.fn.parallaxIt = function(options) {
        var o = $.extend({}, defaultOptions, options);
        var self = $(this);

        // Offset the background based on window scroll
        function position() {
            var yOffset = window.pageYOffset * o.speed;
            self.css('background-position',
                "50% " + yOffset + 'px'
            );
        }

        // Initialize it
        position();

        // Update after any scrolling occurs
        $(document).ready(function() {
            $(window).on('scroll', function() {
                position();
            });
        });
    };

})(jQuery);
