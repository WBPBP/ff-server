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
	console.log(user);
    db.all('SELECT * from user INNER JOIN report on report.user_email = user.user_email WHERE user.user_email = ? ',user, function(err,db_data){
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
			db.run('DELETE from user from user INNER JOIN report ON report.user_email = user.user_email where report.user_email =?', user,function(err){
				if(err){
					console.log("jj");
				}
				else{
					console.log("jj2");}
					
				
			
				});
			}
			// db.run('DELETE from report WHERE report.user_email=? ', user,function(err){
				// if(err){
					// res.send(500);
					// console.log("dd3")
				// }
				// else{
					// res.send(200);
					// console.log("success to delete your email : "+user);
					// console.log("jj2");
				// }
			 //}
		
		
	});
	

		

		
		
});





module.exports = router;