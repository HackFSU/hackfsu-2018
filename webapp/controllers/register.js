//  /register
//

const express = require('express'),
    router = express.Router();

router.get('/', (req, res) => {
    res.render('register/register.pug', {
        title: 'Register'
    });
});

module.exports = router;
