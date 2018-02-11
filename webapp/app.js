const express           = require('express');
const flash             = require('express-flash');
const cookieParser      = require('cookie-parser');
const favicon           = require('serve-favicon');
const logger            = require('morgan');
const sassMiddleware    = require('node-sass-middleware');
const session           = require('express-session');
const path              = require('path');

const app = express();

//
//  Dev. vs Prod. Config
//

let env = process.env.NODE_ENV || 'production';
app.set('env', env);
console.log('Starting in', env, 'mode.');

if (env === 'development') {
    // https://www.npmjs.com/package/dotenv#what-happens-to-environment-variables-that-were-already-set
    require('dotenv').config({path: '../.env'});
}


//
//  App Settings
//

app.set('api-host', process.env.API_HOST);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');


//
//  Middleware
//

app.use(favicon(path.join(__dirname, 'public', 'img/icon.png')));
app.use(logger('dev'));

app.use(cookieParser());
app.use(session({
    cookie: { maxAge: 60000 },
    resave: false,
    secret: process.env.APP_SECRET,
    saveUninitialized: false
}));
app.use(flash());

app.use(sassMiddleware({
    src: path.join(__dirname, 'public/sass'),
    dest: path.join(__dirname, 'public/css'),
    indentedSyntax: true, // true = .sass and false = .scss
    sourceMap: true,
    debug: true,
    prefix: '/css'
}));

//
//  Routing + Helpers
//

app.use(express.static(path.join(__dirname, 'public')));
app.use('/', require('./controllers'));


//
//  Startup
//

app.listen(3000, () => {
    console.log('Express Webapp listening on port 3000');
});
