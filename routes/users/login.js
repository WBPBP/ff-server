var express = require('express');
var app = express();
var router = express.Router();
var bodyParser = require('body-parser');
var sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');


const db = new sqlite3.Database('/home/ec2-user/myapp/data/user.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log(err);
    } else {
    }
});

router.get('/', function (req, res, next) {
    res.render('login');
	
});

//로그인 하는 라우터 
router.post('/in', function (req, res, next) {
	//사용자가 입력한 아이디 비밀번호 
	var id = req.body.user_email;
	var pwd = req.body.user_pwd;
	//메일이 없을때 타입오류 나느데 어떻게 처리할까나 ㅠㅠㅠㅠ 
	db.all('SELECT * from user WHERE user_email = ?',id, function(err,db_data){
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
			//db 에 저장되어있는 id, pwd,salt 불러온다.
				var user = {
			 email_ID : db_result[0]["user_email"], 
			 user_PWD : db_result[0]["user_pwd"],
			 displayName : 'wbpbp'			 
			}
			
			let user_salt = db_result[0]["salt"];
			if (user.email_ID === id) {
				crypto.pbkdf2(pwd,user_salt, 100000, 64, 'sha512', function (err, hashed) {
					let saltPWD = hashed.toString('base64');
					if (saltPWD === user.user_PWD) {
						req.session.displayName = user.email_ID;
						console.log('login success');
						res.sendStatus(200);
					} 
					else {
						console.log('login failure');
						res.sendStatus(400);
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
router.get('/out',function(req,res,next){
	delete req.session.displayName;
	
	res.sendStatus(200);
	console.log('logout');
	}); 

   module.exports = router;




