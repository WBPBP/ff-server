var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } else {
        console.log('connected database in delete.js');
    }
});

router.get('/', function (req, res, next) {
    res.render('delete');
});

router.delete('/', function (req, res, next) {
	db.get("PRAGMA foreign_keys = ON");
	var user = req.body.user_email;
	db.run('DELETE FROM user WHERE user_email = ? ',user,function(err){
		if(err){
			res.sendStatus(500);
		}
		else{
			res.sendStatus(200);
		}			
	});
});
			
module.exports = router;