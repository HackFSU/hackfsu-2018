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
app.use('/static', express.static(path.join(__dirname, './build')));
app.use('/static', express.static(path.join(__dirname, './static')));


/**
 * Render static views
 */
app.get('/', function(req, res) { res.sendFile(path.join(__dirname, './build/views/index/index.html')); } );
app.get('/register', function(req, res) { res.sendFile(path.join(__dirname, './build/views/register/register.html')); } );


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