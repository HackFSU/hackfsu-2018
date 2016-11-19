/**
 * Pug build locals
 */

var locals = {};

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
    instagram: 'https://www.instagram.com/hackfsu'
};

locals.navLinks = {
    index: [
        { name: 'REGISTER', url: '#faq' },
        { name: 'FAQ', url: '#faq' },
        { name: 'SPONSORS', url: '#sponsors' },
        { name: 'HELP', url: '#' },
        { name: 'LOGIN', url: '#' }
    ],

    // For regular non-index pages
    standard: [
        { name: 'Link 1', url: '#' },
        { name: 'Link 2', url: '#' },
        { name: 'Link 3', url: '#' },
        { name: 'Link 4', url: '#' },
        { name: 'Link 5', url: '#' }
    ]
};

module.exports = locals;
