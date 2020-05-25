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
	var user = req.body.user_email;
    db.all('SELECT user_email from user a INNER JOIN report b on a.user_email = b.user_email WHERE a.user_email = ?',user, function(err,db_data){
		db_result=db_data;
		console.log(db_result);
		if(err){
			res.send(500);
			console.log("dd");
		}
		else if(db_result.length==0){
			res.send(401);
			console.log("your email is not existed");
		}
		else{
			db.run('DELETE FROM user INNER JOIN report on user.user_email = report.user_email WHERE user_email = ?',user,function(err,db_data){
				if(err){
					res.send(500);
					console.log("dd3")
				}
				else{
					res.send(200);
					console.log("success to delete your email : "+user);
				}
			});
		}
	});
	
	
		

		
		
});





module.exports = router;