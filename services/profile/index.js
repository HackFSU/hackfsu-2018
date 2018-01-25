const bodyParser        = require('body-parser');
const dotenv            = require('dotenv');
const express           = require('express');
const methodOverride    = require('method-override');
const mongoose          = require('mongoose');
const morgan            = require('morgan');
const qr                = require('qrcode');

const hackerID  = require('./routes/hackerID');

dotenv.config();
console.log('Connecting to database on: ', process.env.DBURI);

// Connect to MongoDB
mongoose.Promise = Promise;
mongoose.connect(process.env.DBURI).then(() => {


    const server = express();
    server.use(bodyParser.json());
    server.use(methodOverride());
    server.use(morgan('common'));

    // Routing
    const router = express.Router();
    router.get('/:hackerID', hackerID);


    server.use(router);
    server.listen(3000, () => {
        console.log('Express Code/QR service listening on port 3000');
    });

}).catch(console.error.bind(console, 'connection error:'));
