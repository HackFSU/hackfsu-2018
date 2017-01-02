/**
 * Pug build locals
 */

var moment = require('moment');

var locals = {};

locals.moment = moment;

locals.baseTitle = 'HackFSU';
locals.getTitle = function(subtitle) {
    if (subtitle && subtitle.length > 0) {
        return locals.baseTitle + ' - ' + subtitle.trim();
    }
    return locals.baseTitle;
};

locals.links = {
    twitter: 'http://www.twitter.com/HackFSU',
    facebook: 'https://www.facebook.com/hackfsu',
    instagram: 'https://www.instagram.com/hackfsu',
    github: 'https://github.com/HackFSU'
};

locals.navLinks = {
    index: [
        { name: 'Register', url: '/register' },
        { name: 'About', url: '#about' },
        { name: 'Sponsors', url: '#sponsors' },
        { name: 'FAQs', url: '#faqs' }
    ],

    indexDayOf: [
        { name: 'Register', url: '/register' },
        { name: 'About', url: '#about' },
        { name: 'Sponsors', url: '#sponsors' },
        { name: 'FAQs', url: '#faqs' },
        { name: 'Help', url: '/help' },
        { name: 'Login', url: '/user/login' }
    ],

    // For regular non-index pages
    standard: [
        { name: 'Register', url: '/register' },
        { name: 'About', url: '/#about' },
        { name: 'Sponsors', url: '/#sponsors' },
        { name: 'FAQs', url: '/#faqs' },
        { name: 'Help', url: '/help' },
        { name: 'Login', url: '/user/login' }
    ]
};

module.exports = locals;
