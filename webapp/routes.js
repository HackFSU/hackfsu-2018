var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

/* GET registration page. */
router.get('/registration', function(req, res, next) {
  res.render('registration', { title: 'registration page' });
});


module.exports = router;
