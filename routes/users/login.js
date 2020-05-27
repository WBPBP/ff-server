var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');

const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } else {
        //console.log('connected database in login.js ');
    }
});

router.get('/', function (req, res, next) {
    res.render('login');
	
});

//로그인 하는 라우터 
router.post('/', function (req, res, next) {
	//아이디 있는지 체크
	var user = req.body.user_email;
	var pwd = req.body.user_pwd;
	//메일이 없을때 타입오류 나느데 어떻게 처리할까나 ㅠㅠㅠㅠ 
	db.all('SELECT * from user WHERE user_email = ?',user, function(err,db_data){
		db_result=db_data;
		//에러 처리
		if(err){
			res.sendStatus(500);
		}
		else if(db_result==0){
			res.sendStatus(401);
			console.log("your email is wrong")
			
		}
		else {
			let email_ID = db_result[0].user_email; //가입되어있는 아이디
			let user_PWD = db_result[0].user_pwd; //가입되어있는 비밀번호
			if (email_ID === user) {
				crypto.randomBytes(32, (err, buffer) => {
					if (err) {
						res.sendStatus(500);
					}
					else {
						crypto.pbkdf2(pwd, salt, 100000, 64, 'sha512', function (err, hashed) {
							let saltPWD = hashed.toString('base64');
							if (saltPWD === user_PWD) {
								req.session.userEmail = user;
								console.log('login success');
								res.sendStatus(200);
							} else {
								console.log('login failure');
								res.sendStatus(400);
							}
						});
					}
				});
			}
			else{
				console.log('this email is not existed');
				res.sendStatus(401);
			}
		}
	});
});

//로그인 하는 라우터. 세션종료 
router.get('/logout',function(req,res,next){
	req.session.destroy(function(err){
		if(err){
			res.sendStatus(500);
		}
		else{
			res.clearCookie('sid');
			res.sendStatus(200);
			req.redirect('/login');
		}
	}); //콜백함수는 세션이 다 종료된 다음 호출이 된다. 
});

   module.exports = router;




