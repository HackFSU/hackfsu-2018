const express           = require('express');
// const bodyParser        = require('body-parser');
const cookieParser      = require('cookie-parser');
const favicon           = require('serve-favicon');
const logger            = require('morgan');
const sassMiddleware    = require('node-sass-middleware');
const path              = require('path');

const app = express();

// Set up dev vs prod
let env = process.env.NODE_ENV || 'production';
app.set('env', env);

let apiHost = env === 'development'
    ? 'http://localhost:8080'
    : 'https://api.hackfsu.com';
app.set('api-host', apiHost);

console.log('Starting in', env, 'mode.');

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

//
//  Middleware
//

app.use(favicon(path.join(__dirname, 'public', 'img/icon.png')));
app.use(logger('dev'));
// Disabled in favor of installing on individual routes??
// app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
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
