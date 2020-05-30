var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } else {
    }
});

router.get('/', function (req, res, next) {
    res.render('delete');
});

router.delete('/', function (req, res, next) {
	db.get("PRAGMA foreign_keys = ON");
	if(req.session.displayName){
	db.run('DELETE FROM user WHERE user_email = ? ',req.session.displayName,function(err){
		if(err){
			res.sendStatus(500);
		}
		else{
			res.sendStatus(200);
		}			
	});
	}
	else{
		console.log('session is expired');
		res.sendStatus(401); //인증이 필요.. 
	}
});
			
module.exports = router;