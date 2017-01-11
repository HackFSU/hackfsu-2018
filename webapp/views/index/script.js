(function() {
    'use strict';

    /**
     * FAQ Text Toggling
     */
    var faqs = $('.faq-item-box');
    var activeClass = 'active';
    faqs.on('click', function() {
        faqs.filter('.' + activeClass).not(this).removeClass(activeClass);
        $(this).toggleClass(activeClass);
    });

    $('#content-container').parallaxIt();
})();
