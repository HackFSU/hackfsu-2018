var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'HackFSU 5' });
});

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

/* GET registration page. */
router.get('/register', function(req, res, next) {
  res.render('register/register', { title: 'Registration Page' });
});


module.exports = router;
