//  /profile routes
//
//  Also includes /login, /logout, etc.
//

const bodyParser    = require('body-parser');
const express       = require('express');
const request       = require('request');

const router = express.Router();

//
//  Login

router.get('/login', (req, res) => {

    res.render('profile/login.pug', {
        title: 'HackFSU 5 | Log In'
    });

});

router.post('/login', (req, res) => {
    let host = req.app.get('api-host');

    req.pipe(request.post(host + '/api/user/login'))
        .on('response', (resp) => {
            // let Location = '/';
            res.set(resp.headers);
            res.redirect('/profile');
        });

});


//
// Profile

router.get('/profile', (req, res) => {
    let host = req.app.get('api-host');

    req.pipe(request.get(host + '/api/user/get/profile', {}, (err, resp, body) => {
        res.send(body);
    }));

});


module.exports = router;
