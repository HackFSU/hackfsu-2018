const request = require('request');

module.exports = function (req, res, next) {
    let host = req.app.get('api-host');

    if (!('sessionid' in req.cookies) && !('csrftoken' in req.cookies)) {
        res.redirect('/login');
        return;
    }

    req.pipe(request.get(host + '/api/user/get/profile', {}, (err, resp, body) => {
        if (resp.statusCode == 200) {
            req.profile = body;
            next();
        } else {
            res.redirect('/login');
        }
    }));

};
