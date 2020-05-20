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
	
	var user = req.body.user_name;
    db.run('DELETE FROM user WHERE user_name = ?',user,function(err,db_data){
		if(err==null&&user!=null)// 손봐야함.. 흠.... 이미 지워진 애들도 지워졌다고 알려주느느 바보... 
		{
			console.log('delete user : '+user);
			res.send('delete user success');
			db.serialize();
		}
		
		else{
			console.log(err);
			console.log('delete failure');
			res.send(-1);
		}
		
    });
});





module.exports = router;