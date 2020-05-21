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
		if(err){
			res.send(500);
		}
		else{//401
		db_result=db_data;
		let user_email = db_result[0].user_email;
		console.log(user_email);
		}
	});
	
	
	crypto.randomBytes(32,(err,buffer)=>{
		if(err){
			res.send(500);
		}
		else{
			db.all('SELECT * FROM user WHERE user_email = ?',user,function(err,db_data){ //아이디에 해당하는 정보 불러오기
				
				 //db에 저장된 salt,hash비밀번호 가져옴 
				  db_result = db_data;
				  let salt = db_result[0].salt; //
				  let user_pwd = db_result[0].user_pwd;
				  console.log(salt);
				 
				 
				  crypto.pbkdf2(pwd,salt,100000,64,'sha512', function(err,hashed){
					  let saltPWD =hashed.toString('base64');
					  if (saltPWD==user_pwd) {
						req.session.is_logined = true;
						req.session.save(function(req,res,next){
						  console.log('save');
						});  
						console.log('login success');
						res.send(200);
					  } 
					  else{
						console.log('login failure'); 
						res.send(400);
					  }
				  });
				
				  
			  
			});
			
		}
    
	});
});

//로그인 하는 라우터. 세션종료 
router.get('/logout',function(req,res,next){
	req.session.destroy(function(err){
		req.redirect('/');
	}); //콜백함수는 세션이 다 종료된 다음 호출이 된다. 
});

   module.exports = router;




