const express = require('express'),
    router = express.Router();

//  Index page
router.get('/', (req, res) => {
    res.render('index', {
        title: 'HackFSU 5'
    });
});

//  Other routes
router.use('/register', require('./register'));
router.use(require('./profile'));

//  Error Handling
router.use(require('./errors'));

module.exports = router;
