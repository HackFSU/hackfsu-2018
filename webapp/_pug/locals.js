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
        { name: 'FAQ', url: '#faq' }
    ],

    indexDayOf: [
        { name: 'Register', url: '/register' },
        { name: 'About', url: '#about' },
        { name: 'Sponsors', url: '#sponsors' },
        { name: 'FAQs', url: '#faq' },
        { name: 'Help', url: '/help' },
        { name: 'Login', url: '/user/login' }
    ],

    // For regular non-index pages
    standard: [
        { name: 'Register', url: '/register' },
        { name: 'About', url: '/#about' },
        { name: 'Sponsors', url: '/#sponsors' },
        { name: 'FAQs', url: '/#faq' },
        { name: 'Help', url: '/help' },
        { name: 'Login', url: '/user/login' }
    ]
};

// Sponsors for this year only (doesnt matter if repeated in pastSponsors)
locals.currentSponsors = {
    1: [
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"}
    ],
    2: [
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"}
    ],
    3: [
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"}
    ]
};

// Sponsors from previous years
locals.pastSponsors = {
    2016: [
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"}
    ],

    2015: [
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"}
    ],

    2014: [
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"}
    ],

    2013: [
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"},
        {name: "TODO", imgSrc: "/static/img/logos/hackfsu-white.png", href: "#TODO"}
    ]

};


module.exports = locals;
