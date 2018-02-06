//  /profile routes
//
//  Also includes /login, /logout, etc.
//

const bodyParser    = require('body-parser');
const cookieParser  = require('cookie-parser');
const express       = require('express');
const request       = require('request');

//
//  Three routers:
//      authRouter:     Primary router handling auth-related paths.
//      loginRouter:    Router for logging in and out.
//      profileRouter:  These routes require user to be logged in.

const authRouter = express.Router();
const loginRouter = express.Router();
const profileRouter = express.Router();

authRouter.use(bodyParser.urlencoded({ extended: true }));
authRouter.use(bodyParser.json());
authRouter.use(cookieParser());
authRouter.use('/profile', profileRouter);
authRouter.use(loginRouter);

profileRouter.use(require('../middleware/auth'));


//
//  Login

loginRouter.get('/login', (req, res) => {
    let msg = decodeURIComponent(req.query.msg);
    console.log('msg', msg);

    res.render('profile/login.pug', {
        title: 'HackFSU 5 | Log In',
        msg: msg
    });
});

loginRouter.post('/login', (req, res) => {
    let host = req.app.get('api-host');

    // console.log(req.body.email);
    let email = req.body.email,
        password = req.body.password;

    request.post(host + '/api/user/login',
        { json: { email, password }},
        (err, resp, body) => {

            // Successful login
            if (resp.statusCode === 200) {
                res.set(resp.headers);
                res.redirect('/profile');
            }

            // Bad login
            else {
                let msg = encodeURIComponent('Incorrect username or password.');
                res.redirect(`/login?msg=${msg}`);
            }
        });

});

loginRouter.get('/logout', (req, res) => {
    let host = req.app.get('api-host');
    res.clearCookie('sessionid');
    res.clearCookie('csrftoken');
    res.redirect('/');
});

//
// Profile

profileRouter.get('/', (req, res) => {

    res.json(JSON.parse(req.profile));
    // let host = req.app.get('api-host');

    // req.pipe(request.get(host + '/api/user/get/profile', {}, (err, resp, body) => {
    //     res.send(body);
    // }));

});


module.exports = authRouter;
