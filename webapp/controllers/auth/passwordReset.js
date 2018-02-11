const request       = require('request');
const { CookieJar } = require('tough-cookie');

const start = {
    GET: function (req, res) {
        res.render('profile/password_reset/start.pug', {
            title: 'HackFSU 5 | Reset Password'
        });
    },

    POST: function (req, res) {
        let host = req.app.get('api-host');
        request.post(host + '/api/user/password/reset/start',
            {
                json: {
                    email: req.body.email,
                    g_recaptcha_response: req.body['g-recaptcha-response']
                }
            },
            (err, resp) => {
                if (!err && resp.statusCode === 200) {
                    req.flash('info', 'An email will been sent to the given address if the account exists.');
                    res.redirect('/login');
                }

                else {
                    console.log('err:', err);
                    req.flash('error', 'Whoops, there\'s been an error. Please contact us.');
                    res.redirect('/');
                }
            }
        );
    },
};

const finish = {
    GET: function (req, res) {
        let host = req.app.get('api-host'),
            jar = request.jar();

        req.pipe(request.get(host + `/user/password/reset/${req.params.link_key}`,
            { jar: jar },
            (err, resp) => {

                // Serialzie the jar and pass to session
                req.session.jar = jar._jar.toJSON();

                if (!err && resp.statusCode === 200) {
                    // If someone comes knocking on an invalid link.
                    try {
                        if (resp.request.uri.query === 'accessDenied=true') {
                            req.flash('error', 'Invalid link.');
                            res.redirect('/login');
                            return;
                        }
                    }
                    catch(err) {
                        //
                    }

                    res.render('profile/password_reset/finish.pug', {
                        title: 'HackFSU 5 | Reset Password'
                    });
                }

                else {
                    console.log('err:', err);
                    req.flash('error', 'Whoops, there\'s been an error. Please contact us.');
                    res.redirect('/');
                }
            }
        ));
    },

    POST: function (req, res) {
        let host = req.app.get('api-host'),
            toughCookieJar = CookieJar.fromJSON(req.session.jar),
            requestJar = request.jar();

        // Substitute the default internals for one with the data we want.
        requestJar._jar = toughCookieJar;

        request.post(host + '/api/user/password/reset/complete',
            {
                json: { new_password: req.body.password },
                jar: requestJar
            },
            (err, resp) => {
                if (!err && resp.statusCode === 200) {
                    req.flash('info', 'Password successfully changed.');
                    res.redirect('/login');
                }

                else {
                    console.log('err:', err);
                    req.flash('error', 'Whoops, there\'s been an error. Please contact us.');
                    res.redirect('/');
                }
            }
        );
    }
};

module.exports = {
    start,
    finish
};
