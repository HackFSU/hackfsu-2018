const express           = require('express');
const bodyParser        = require('body-parser');
const cookieParser      = require('cookie-parser');
const favicon           = require('serve-favicon');
const logger            = require('morgan');
const sassMiddleware    = require('node-sass-middleware');
const path              = require('path');

const app = express();

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

//
//  Middleware
//

//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
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
