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

locals.keys = {
    reCaptchaSiteKey: '6LffORIUAAAAAL0tK0lbV9sJ1AWO5Q_FMBNh51Dv'
};

locals.links = {
    twitter: 'http://www.twitter.com/HackFSU',
    facebook: 'https://www.facebook.com/hackfsu',
    instagram: 'https://www.instagram.com/hackfsu',
    github: 'https://github.com/HackFSU',
    sponsorshipPacket: '/static/res/HackFSU_sponsorship_options_spring_2017.pdf',
    mlh: {
        codeOfConduct: 'https://static.mlh.io/docs/mlh-code-of-conduct.pdf',
        contestTerms: 'https://github.com/MLH/mlh-policies/tree/master/prize-terms-and-conditions',
        privatePolicy: 'https://mlh.io/privacy'
    }
};

locals.emails = {
    info: 'info@hackfsu.com',
    sponsors: 'sponsors@hackfsu.com',
    travel: 'travel@hackfsu.com',
    dev: 'dev@hackfsu.com'
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

    error: [
        { name: 'Home', url: '/' }
    ],

    // For regular non-index pages
    standard: [
        { name: 'Register', url: '/register' },
        // { name: 'Help', url: '/help' },
        { name: 'Login', url: '/user/login' }
    ],

    // For regular user pages
    user: [
        { name: 'Profile', url: '/user/profile' },
        { name: 'Logout', url: '/user/logout' }
    ]
};


/**
 * Sponsor Data
 * See the respective markdown info files for each year in /static/img/logos
 *
 * Logo should be the company's most current, if we have it.
 */
var sponsorData = locals.sponsorData = {
    accenture: {
        name: 'Accenture',
        href: 'http://www.accenture.com',
        logo: '/static/img/logos/accenture.png'
    },
    acmAtFsu: {
        name:'ACM at FSU',
        href: 'https://www.facebook.com/groups/cs.fsu.acm/',
        logo: '/static/img/logos/acm-at-fsu.png',
        logoStyle: 'padding: 20px;'
    },
    apple: {
        name: 'Apple',
        href: 'http://www.apple.com/',
        logo: '/static/img/logos/apple.png',
        logoStyle: 'padding: 0 75px;'
    },
    codeSchool: {
        name: 'Code School',
        href: 'https://www.codeschool.com/',
        logo: '/static/img/logos/code-school.png'
    },
    domiStation: {
        name: 'Domi Station',
        href: 'https://www.domistation.com',
        logo: '/static/img/logos/domi-station.png'
    },
    fitc: {
        name: 'Florida IT Career Alliance (FITC)',
        href: 'http://fitc.cci.fsu.edu/',
        logo: '/static/img/logos/fitc.png'
    },
    fsuCollegeOfArtsAndSciences: {
        name: 'FSU College of Arts & Sciences',
        href: 'http://artsandsciences.fsu.edu/',
        logo: '/static/img/logos/fsu-arts-sciences.png'
    },
    genivia: {
        name: 'Genivia',
        href: 'http://www.genivia.com/',
        logo: '/static/img/logos/genivia.png'
    },
    giantIvy: {
        name: 'GiantIVY',
        href: 'http://www.giantivy.com/',
        logo: '/static/img/logos/giant-ivy.jpg'
    },
    hashrocket: {
        name: 'Hashrocket',
        href: 'http://hashrocket.com/',
        logo: '/static/img/logos/hashrocket.png'
    },
    ionicSecurity: {
        name: 'Ionic Security',
        href: 'https://www.ionic.com/',
        logo: '/static/img/logos/ionic-security.jpg'
    },
    jmi: {
        name: 'The Jim Moran Institute For Global Entrepreneurship (JMI)',
        href: 'http://business.fsu.edu/jmi',
        logo: '/static/img/logos/jmi.png'
    },
    lob: {
        name: 'Lob',
        href: 'http://lob.com/',
        logo: '/static/img/logos/lob.png',
        logoStyle: 'padding: 0 25px;'
    },
    mailChimp: {
        name: 'MailChimp',
        href: 'http://mailchimp.com/',
        logo: '/static/img/logos/mailchimp.jpg'
    },
    mlh: {
        name: 'Major League Hacking (MLH)',
        href: 'https://mlh.io/seasons/na-2017/events', /* current season */
        logo: '/static/img/logos/mlh/mlh-logo-color.png',
        badge: '/static/img/logos/mlh/mlh-badge-white.png',
        external: {
            badge: 'https://s3.amazonaws.com/logged-assets/trust-badge/2017/white.svg'
        }
    },
    namecheap: {
        name: 'Namecheap',
        href: 'http://namecheap.com/',
        logo: '/static/img/logos/namecheap.png'
    },
    oei: {
        name: 'Office of Entrepreneurship and Innovation (OEI)',
        href: 'http://sga.fsu.edu/oei/',
        logo: '/static/img/logos/oei.png',
        logoStyle: 'padding: 0 40px;'
    },
    sds: {
        name: 'Strategic Digital Services (SDS)',
        href: 'http://strategicdigitalservices.net/',
        logo: '/static/img/logos/sds.png'
    },
    selenko: {
        name: 'Selenko',
        href: 'http://www.selenko.com/',
        logo: '/static/img/logos/selenko.png'
    },
    seminoleDining: {
        name: 'Seminole Dining',
        href: 'http://www.seminoledining.com',
        logo: '/static/img/logos/seminole-dining.png'
    },
    soylent: {
        name: 'Soylent',
        href: 'https://www.soylent.com',
        logo: '/static/img/logos/soylent.png'
    },
    starbucksAndRenegadeRunner: {
        name: 'Starbucks and Renegade Runner',
        href: 'https://www.fsudelivery.com/',
        logo: '/static/img/logos/starbucks-and-renegade-runner.png'
    },
    stateFarm: {
        name: 'State Farm',
        href: 'http://www.statefarm.com',
        logo: '/static/img/logos/state-farm.png'
    },
    talTech: {
        name: 'TalTech Alliance',
        href: 'http://www.taltech.org/',
        logo: '/static/img/logos/taltech.png'
    },
    techNole: {
        name: 'TechNole',
        href: 'https://nolecentral.dsa.fsu.edu/organization/technole',
        logo: '/static/img/logos/technole/technole-horizontal.png'
    },
    theCrepeVine: {
        name: 'The Crepe Vine',
        href: 'http://www.thecrepevine.com/',
        logo: '/static/img/logos/the-crepe-vine.png'
    },
    uberOperations: {
        name: 'Uber Operations LLC',
        href: 'http://uberops.com/',
        logo: '/static/img/logos/uber-operations-llc.png'
    },
    valeFoodCo: {
        name: 'Vale Food Co.',
        href: 'http://valefoodco.com/',
        logo: '/static/img/logos/vale-food-co.png'
    },
    wolfram: {
        name: 'Wolfram',
        href: 'http://www.wolfram.com/',
        logo: '/static/img/logos/wolfram.png'
    }
};

// Locals for pug use
locals.sponsors = {
     '2017': {
        sponsors: {
            '3': [],
            '2': [],
            '1': []
        },
        partners: [
            sponsorData.techNole,
            sponsorData.mlh,
            sponsorData.acmAtFsu
        ]
    },

    '2016': {
        sponsors: {
            '3': [
                sponsorData.apple
            ],
            '2': [
                sponsorData.stateFarm,
                sponsorData.accenture,
                sponsorData.jmi
            ],
            '1': [
                sponsorData.genivia,
                sponsorData.sds,
                sponsorData.codeSchool,
                sponsorData.domiStation,
                sponsorData.soylent,
                sponsorData.seminoleDining
            ]
        },
        partners: [
            sponsorData.techNole,
            sponsorData.mlh,
            sponsorData.fsuCollegeOfArtsAndSciences
        ]
    },

    '2015': {
        sponsors: {
            '3': [
                sponsorData.mailChimp,
                sponsorData.ionicSecurity
            ],
            '2': [
                sponsorData.valeFoodCo,
                sponsorData.domiStation,
                sponsorData.starbucksAndRenegadeRunner,
                sponsorData.codeSchool
            ],
            '1': [
                sponsorData.uberOperations,
                sponsorData.oei,
                sponsorData.fitc,
                sponsorData.jmi,
                sponsorData.sds,
                sponsorData.talTech
            ]
        },
        partners: [
            sponsorData.techNole,
            sponsorData.mlh
        ]
    },

    '2014': {
        sponsors: {
            '2': [
                sponsorData.domiStation
            ],
            '1': [
                sponsorData.selenko,
                sponsorData.theCrepeVine,
                sponsorData.jmi,
                sponsorData.hashrocket,
                sponsorData.wolfram,
                sponsorData.namecheap,
                sponsorData.lob,
                sponsorData.giantIvy
            ]
        },
        partners: [
            sponsorData.techNole
        ]
    }
};


/**
 * User Registration Form options
 */
 locals.shirt_size_choices = {
    'm-s':     'Men\'s Small',
    'm-m':     'Men\'s Medium',
    'm-l':     'Men\'s Large',
    'm-xl':    'Men\'s XL',
    'm-2xl':   'Men\'s XXL',
    'm-3xl':   'Men\'s XXXL',
    'w-s':     'Women\'s Small',
    'w-m':     'Women\'s Medium',
    'w-l':     'Women\'s Large',
    'w-xl':    'Women\'s XL'
};

locals.anon_stats = {
	"ethnicity": {
		"white": "White",
		"asian": "Asian",
		"hispanic": "Hispanic",
		"black": "Black",
		"multicultural": "Multicultural",
		"other": "Other"
	},
	"gender": {
		"male": "Male",
		"female": "Female",
		"other": "Other"
	}
};

/**
 * Hacker Registration Form options
 */

locals.student_types = {
    'college': 'College Student',
    'highschool': 'High School Student',
    'graduated': 'Recent College Graduate'
};

locals.school_year_choices = {
    'FR': 'Freshman',
    'SO': 'Sophomore',
    'JR': 'Junior',
    'SR': 'Senior',
    'SS': '\"Super Senior\"',
    'GS': 'Graduate Student'
};
locals.school_year_choices_all = {
    'FR': 'Freshman',
    'SO': 'Sophomore',
    'JR': 'Junior',
    'SR': 'Senior',
    'SS': '\"Super Senior\"',
    'GS': 'Graduate Student',
    'RG': 'Recent College Graduate',
    'HS': 'High School Student'
};

locals.job_seeker_options = {
    'full-time' : 'Full-time',
    'part-time' : 'Part-time',
    'internship' : 'Internship',
    'none' : 'No'
};


locals.options = {
    mentor_availability: {},
    project_types: [
        'Front-End',
        'Back-End',
        'Web',
        'Hardware',
        'iOS',
        'Android',
        'Virtual Reality',
        'Design'
    ]
};

// Keys as bit flags
locals.options.mentor_availability[''+Math.pow(2,0)] = 'Friday - Late Night';
locals.options.mentor_availability[''+Math.pow(2,1)] = 'Saturday - Early Morning';
locals.options.mentor_availability[''+Math.pow(2,2)] = 'Saturday - Morning';
locals.options.mentor_availability[''+Math.pow(2,3)] = 'Saturday - Afternoon';
locals.options.mentor_availability[''+Math.pow(2,4)] = 'Saturday - Night';
locals.options.mentor_availability[''+Math.pow(2,5)] = 'Saturday - Late Night';
locals.options.mentor_availability[''+Math.pow(2,6)] = 'Sunday - Early Morning';
locals.options.mentor_availability[''+Math.pow(2,7)] = 'Sunday - Morning';
locals.options.mentor_availability[''+Math.pow(2,8)] = 'Sunday - Afternoon';




module.exports = locals;
