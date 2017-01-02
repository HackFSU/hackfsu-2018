/**
 * Simple express app to mimic backend. For testing only.
 */

var http = require('http');
var express = require('express');
var morgan = require('morgan');
var path = require('path');

var app = express();
var port = 5000;

function boot() {
    var server = http.createServer(app);

    server.on('listening', function() {
        console.log('Server Live @ http://localhost:' + port);
    });

    server.listen(port);
}

app.use(morgan('dev'));
app.use('/static', express.static(path.join(__dirname, './build/static')));
app.use('/static', express.static(path.join(__dirname, './static')));


/**
 * Render static views
 */
function getStaticView(getPath, viewPath) {
    app.get(getPath, function(req, res) {
        res.sendFile(path.join(__dirname, './build/views/'+viewPath+'/index.html'));
    });
}

var staticViews = [
    { getPath: '/', viewPath: 'index' },
    { getPath: '/register', viewPath: 'register' },
    { getPath: '/help', viewPath: 'help' },
    { getPath: '/user/login', viewPath: 'user/login' },
    { getPath: '/user/profile', viewPath: 'user/profile' },
    { getPath: '/error/404', viewPath: 'error/404' },
    { getPath: '/error/500', viewPath: 'error/500' }
];

staticViews.forEach(function(view) {
    getStaticView(view.getPath, view.viewPath);
});

// Redirect shortcuts
app.get('/login', function(req, res) { res.redirect('/user/login'); });


/**
 * Mock api
 */





/**
 * Direct boot if run from node command
 */
if (require.main === module) {
    boot();
}

module.exports = {
    boot: boot,
    app: app
};
