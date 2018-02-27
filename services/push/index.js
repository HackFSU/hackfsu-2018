const bodyParser        = require('body-parser');
const dotenv            = require('dotenv');
const express           = require('express');
const methodOverride    = require('method-override');
const mongoose          = require('mongoose');
const morgan            = require('morgan');
const qr                = require('qrcode');

//  When not launching production mode, we want to load our
//  local .env file; otherwise Docker-Compose uses env_file.
const env = process.env.NODE_ENV || 'development';
if (env === 'development') {
    dotenv.config();
}
const DB_URI = process.env.QR_DB;

console.log('Starting in', env, 'mode.');
console.log('Connecting to database on: ', DB_URI);

// Connect to MongoDB
mongoose.Promise = Promise;
mongoose.connect(DB_URI).then(() => {

    const server = express();
    server.set('env', env);
    server.use(bodyParser.json());
    server.use(methodOverride());
    server.use(morgan('dev'));

    // Routing
    const router = express.Router();
    router.post('/push/register', require('./routes/register'));
    router.post('/push/new', require('./routes/push'));

    server.use(router);
    server.listen(3000, () => {
        console.log('Express Push Device ID service listening on port 3000');
    });

}).catch(console.error.bind(console, 'connection error:'));
