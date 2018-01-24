//  /register
//

const request = require('request');
const express = require('express'),
    router = express.Router();

router.get('/', (req, res) => {
    res.render('register/register.pug', {
        title: 'Register'
    });
});

router.post('/', (req, res) => {

    // VERY IMPORTANT:
    // This will not work if body-parser is enabled
    // upstream.

    let host = req.app.get('api-host');
    let stream = req.pipe(request.post(host + '/api/hacker/register')).pipe(res);

});


module.exports = router;
